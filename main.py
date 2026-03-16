import os
import pandas as pd
import plotly.express as px
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from llm_service import LLMService
from query_executor import QueryExecutor
from report_generator import ReportGenerator

app = FastAPI()
llm = LLMService(api_key=os.getenv('GEMINI_API_KEY', ''))
exec = QueryExecutor()
rep = ReportGenerator()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    with open(f"data/{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"status": "success", "schema": exec.sync_db()}

@app.post("/ask")
async def ask(query: str = None, audio: UploadFile = File(None)):
    if not query and not audio:
        raise HTTPException(status_code=400, detail="query or audio required")

    schema = exec.sync_db()
    schema_meta = exec.get_schema()

    if audio:
        audio_bytes = await audio.read()
        plan = llm.analyze_query(audio_bytes, schema_meta, is_audio=True)
    else:
        plan = llm.analyze_query(query, schema_meta)

    if 'sql' not in plan or not plan['sql']:
        raise HTTPException(status_code=422, detail="Could not generate SQL from query")

    df = exec.run_sql(plan['sql'])
    insight = llm.get_insight(df.head(10).to_string())
    return {"data": df.to_dict(orient="records"), "viz": plan, "insight": insight}


@app.post('/report')
async def report(query: str, insight: str, data: list, viz: dict = None):
    if not data:
        raise HTTPException(status_code=400, detail='Empty data cannot generate report')

    try:
        df = pd.DataFrame(data)
    except Exception as ex:
        raise HTTPException(status_code=400, detail=f'Unable to parse data: {ex}')

    # For simplicity, create a plotly figure from viz or auto-guess
    fig = None
    if viz and viz.get('chart_type') in ['bar', 'line', 'pie'] and viz.get('x') and viz.get('y'):
        if viz['chart_type'] == 'bar':
            fig = px.bar(df, x=viz['x'], y=viz['y'])
        elif viz['chart_type'] == 'line':
            fig = px.line(df, x=viz['x'], y=viz['y'])
        elif viz['chart_type'] == 'pie':
            fig = px.pie(df, names=viz['x'], values=viz['y'])

    # fallback if there is no viz
    if fig is None and not df.empty:
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_columns:
            fig = px.bar(df, x=df.columns[0], y=numeric_columns[0])

    path = rep.generate(query=query, insight=insight, df=df, fig=fig)
    return FileResponse(path, media_type='application/pdf', filename='blackcord_report.pdf')