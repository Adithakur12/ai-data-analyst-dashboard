# Blackcord Data Analyst

A complete end-to-end interactive data analytics hackathon project using FastAPI + Streamlit + SQLite + Gemini + PDF reporting.

## ⭐ Features

- CSV upload and database sync
- Natural language query to SQL with Gemini (or fallback parser)
- Auto chart generation (bar/line/pie)
- Manual chart selection
- Data filtering on query results
- Query history tracking
- AI insight summary
- Download query results (CSV/JSON)
- Generate report PDF via endpoint

## 📁 Project structure

- `main.py` - FastAPI server: `/upload`, `/ask`, `/report`
- `query_executor.py` - CSV sync, SQL execution, schema introspection, SQLite backend
- `llm_service.py` - Gemini integration + offline fallback query to SQL
- `report_generator.py` - PDF generation using `fpdf`
- `frontend.py` - Streamlit UI (Blackcord Data Analyst)
- `requirements.txt` - dependencies
- `data/` - datasets and generated report

## ⚙️ Setup

> Use Python 3.10+ (recommended)
> Either create a venv or run in global environment

### 1. Create and activate virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Optional: set Gemini API key

Create a `.env` file with:

```ini
GEMINI_API_KEY=your_api_key_here
```

or set environment variable directly:

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

## ▶️ Run

### Start backend

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Start frontend

```powershell
streamlit run frontend.py
```

Then open the Streamlit URL printed in the console (usually `http://localhost:8501`).

## 🧩 Use flow

1. Upload CSV(s) via sidebar `Upload CSVs` and click `Sync Database`
2. Enter a natural query or SQL in query area
3. Run query to view chart/table/result
4. Filter results and download data
5. Click `Save Report as PDF` to generate a PDF report
6. View query history and last result details

## 🚀 Develop / test

- FastAPI dev reload in `main.py` enables hot reload
- Add CSV under `data/` or upload through UI
- `query_executor.py` handles all SQL
- `llm_service.py` fallback returns simple select if Gemini is unavailable

## 🐞 Troubleshooting

- `ModuleNotFoundError`: ensure `pip install -r requirements.txt` succeeded
- Uvicorn port conflict: pick another port `--port 8001`
- Streamlit and backend not connected: check `http://localhost:8000` accessibility
- No data in query: confirm CSV has valid rows and columns

## 💡 Notes

- If Gemini API key is not available, local fallback still works with base query parsing
- Data to SQL generation is best-effort, and can be extended with custom logic
- PDF generation uses the `report_generator.ReportGenerator` with chart snapshot

---

Made for hackathon success with robust end-to-end interaction and clean UI.
