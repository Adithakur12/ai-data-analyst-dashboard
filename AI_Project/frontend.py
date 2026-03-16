import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import io
import json
import time

st.set_page_config(page_title="Blackcord Data Analyst", layout="wide")
st.markdown("""
<style>
.reportview-container {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
    color: #ffffff;
}
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #1f2937, #3b82f6);
    color: #f8fafc;
}
.stButton>button {
    background: linear-gradient(90deg, #22c55e, #14b8a6);
    color: white;
    border: 0;
}
.stDownloadButton>button {
    background-color: #6366f1;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🎨 Blackcord Data Analyst")
st.markdown("### A lively, interactive AI analytics experience with theme, widgets, and quick insights.")

if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_df' not in st.session_state:
    st.session_state.last_df = pd.DataFrame()
if 'last_insight' not in st.session_state:
    st.session_state.last_insight = ''
if 'last_sql' not in st.session_state:
    st.session_state.last_sql = ''

# helper for colourful KPI cards
def render_kpis(df):
    if df is None or df.empty:
        return
    n_rows = len(df)
    n_cols = len(df.columns)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    with st.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", n_rows, delta=f"{max(0, n_rows-100)} new")
        c2.metric("Columns", n_cols, delta=f"{max(0, n_cols-5)} added")
        c3.metric("Numeric fields", len(numeric_cols), delta=f"{len(numeric_cols)} available")

# Utility function to automatically pick a chart
def auto_chart(df):
    if df is None or df.empty:
        return None
    numeric = df.select_dtypes(include=['number']).columns.tolist()
    if len(numeric) >= 2:
        x, y = numeric[0], numeric[1]
        return px.scatter(df, x=x, y=y, title=f"Auto chart: {y} vs {x}"), x, y
    if len(numeric) == 1 and 'category' in df.columns:
        return px.bar(df, x='category', y=numeric[0], title="Auto chart"), 'category', numeric[0]
    return None

with st.sidebar:
    st.header("Upload Sources")
    files = st.file_uploader("Upload CSVs", accept_multiple_files=True, type=['csv'])

    st.markdown("---")
    st.subheader("AI Assistant")
    ai_model = st.selectbox("AI Model", ["gpt-4", "gpt-3.5", "local"], index=1)
    ai_context = st.text_area("AI context (optional)", "Provide context for AI to help generate better SQL and insights.", height=80)

    if st.button("Generate query suggestion"):
        if not st.session_state.get('query_input', '').strip():
            st.warning("Please type a base question in the main input first")
        else:
            with st.spinner("Generating AI suggestion..."):
                time.sleep(0.7)
                try:
                    ai_resp = requests.post("http://localhost:8000/suggest", json={
                        'prompt': st.session_state.query_input,
                        'context': ai_context,
                        'model': ai_model
                    }, timeout=5)
                    if ai_resp.status_code == 200:
                        suggested = ai_resp.json().get('suggestion', '')
                    else:
                        suggested = ''
                except Exception:
                    suggested = ''

                st.session_state.suggested_query = suggested or f"Show top 10 records for: {st.session_state.query_input}"
                st.success("Suggestion ready. Edit and run the query.")

    st.markdown("---")
    if st.button("Sync Database"):
        if not files:
            st.error("Please select at least one CSV file")
        else:
            for f in files:
                requests.post("http://localhost:8000/upload", files={"file": f})
            st.success("Database Updated!")

    st.markdown("---")
    st.subheader("Dataset Preview")
    if files:
        for f in files:
            with st.expander(f.name):
                df_sample = pd.read_csv(f)
                st.write(df_sample.head(5))

    st.markdown("---")
    st.subheader("Query History")
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-15:])):
            st.write(f"{len(st.session_state.history)-i}. {item['query']}")
            st.write(f"SQL: {item.get('sql','')}")
            st.write(f"Insight: {item.get('insight','')}")
    else:
        st.write("No history yet")

# Query widget
if 'suggested_query' not in st.session_state:
    st.session_state.suggested_query = ''

query_input = st.text_area("Enter question or SQL query", height=100, value=st.session_state.get('suggested_query', ''), placeholder="e.g., show top 10 products by sales")
st.session_state.query_input = query_input
chart_choice = st.selectbox("Auto chart type or choose", ['auto', 'bar', 'line', 'pie', 'table'])

if st.button("Run Query"):
    progress = st.progress(0)
    status = st.empty()
    status.info("Initializing AI & DB query...")
    progress.progress(10)
    time.sleep(0.2)

    if not query_input.strip():
        status.warning("Please enter a query first")
        progress.empty()
    else:
        status.info("Preparing request payload...")
        progress.progress(30)
        time.sleep(0.2)

        with st.spinner("Executing query..."):
            try:
                status.info("Calling backend API...")
                progress.progress(50)
                res = requests.post(
                    f"http://localhost:8000/ask?query={requests.utils.quote(query_input.strip())}",
                    json={'model': ai_model, 'context': ai_context}
                ).json()
                progress.progress(80)
            except Exception as e:
                status.error("Backend not reachable: " + str(e))
                progress.progress(0)
                res = {}

            if res.get('data') is None:
                status.error(f"No data returned. Response: {res}")
                progress.progress(0)
            else:
                progress.progress(100)
                status.success("Query executed successfully")
                time.sleep(0.1)

                df = pd.DataFrame(res['data'])
                st.session_state.last_df = df
                st.session_state.last_insight = res.get('insight', '')
                st.session_state.last_sql = res.get('viz', {}).get('sql', '')

                st.info(f"AI Insight: {st.session_state.last_insight}")

                render_kpis(df)

                with st.expander("Query details and actions", expanded=True):
                    st.write("**Query:**", query_input.strip())
                    st.write("**Generated SQL:**", st.session_state.last_sql or "-- none")

                # filter controls for non-empty data
                if not df.empty:
                    st.subheader("Filter and Summary Data")
                    filter_col = st.selectbox("Filter column", [None] + list(df.columns), index=0)
                    if filter_col:
                        unique_values = df[filter_col].dropna().unique().tolist()
                        selected_values = st.multiselect(f"Filter {filter_col} values", unique_values, default=unique_values[:5])
                        if selected_values:
                            df = df[df[filter_col].isin(selected_values)]

                st.subheader("Visualization and Results")
                chart_tabs = st.tabs(["Chart", "Table"])

                with chart_tabs[0]:
                    fig = None
                    chart_type = chart_choice
                    viz = res.get('viz', {})

                    if chart_type == 'auto':
                        auto = auto_chart(df)
                        if auto:
                            fig, x_axis, y_axis = auto
                        else:
                            st.warning("Auto chart could not be generated. Select chart manually.")
                    else:
                        x_axis = viz.get('x') if viz.get('x') else (df.columns[0] if len(df.columns) > 0 else None)
                        y_axis = viz.get('y') if viz.get('y') else (df.select_dtypes(include=['number']).columns[0] if len(df.select_dtypes(include=['number']).columns) > 0 else None)
                        try:
                            if chart_type == 'bar' and x_axis and y_axis:
                                fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                            elif chart_type == 'line' and x_axis and y_axis:
                                fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} trend")
                            elif chart_type == 'pie' and x_axis and y_axis:
                                fig = px.pie(df, names=x_axis, values=y_axis, title=f"{x_axis} distribution")
                        except Exception as e:
                            st.warning(f"Could not build chart: {e}")

                    if fig is not None:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No chart available; choose another type or filter differently.")

                with chart_tabs[1]:
                    st.dataframe(df)

                st.download_button("Download CSV", df.to_csv(index=False), file_name="blackcord_result.csv", mime="text/csv")
                st.download_button("Download JSON", df.to_json(orient='records'), file_name="blackcord_result.json", mime="application/json")

                if st.button("Save Report as PDF"):
                    try:
                        payload = {
                            'query': query_input.strip(),
                            'insight': st.session_state.last_insight,
                            'data': df.to_dict(orient='records'),
                            'viz': res.get('viz', {})
                        }
                        response = requests.post("http://localhost:8000/report", json=payload)
                        if response.status_code == 200:
                            st.success("PDF report generated successfully")
                            st.download_button("Download Report", response.content, file_name="blackcord_report.pdf", mime="application/pdf")
                        else:
                            st.error(f"Failed to generate report: {response.text}")
                    except Exception as e:
                        st.error(f"Report generation failed: {e}")

                st.markdown("### Generated SQL (from LLM)")
                st.code(st.session_state.last_sql or "-- no SQL generated", language='sql')

                st.session_state.history.append({
                    'query': query_input.strip(),
                    'sql': st.session_state.last_sql,
                    'insight': st.session_state.last_insight,
                    'rows': len(df)
                })

        status.empty()
        progress.empty()

with st.expander("Last query details"):
    st.write("AI Insight:", st.session_state.last_insight)
    st.write("SQL:", st.session_state.last_sql)
    if not st.session_state.last_df.empty:
        st.write("Rows:", len(st.session_state.last_df))

with st.expander("Saved query history"):
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history[-10:]))
    else:
        st.write("No history yet")

# Data Explorer tab
st.markdown("---")
st.subheader("Data Explorer")
if not st.session_state.last_df.empty:
    st.write("Table preview")
    st.dataframe(st.session_state.last_df.head(50))
else:
    st.write("No data available yet. Run a query first.")