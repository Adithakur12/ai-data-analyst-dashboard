import os
import google.generativeai as genai
import json

class LLMService:
    def __init__(self, api_key=None):
        self.use_remote = bool(api_key and api_key != "YOUR_GEMINI_KEY")
        if self.use_remote:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_query(self, user_input, schema, is_audio=False):
        if is_audio:
            raise ValueError("Audio analysis is not yet implemented in offline fallback mode.")

        if self.use_remote:
            try:
                if not os.path.exists('prompts') or not os.path.exists('prompts/dashboard_prompt.txt'):
                    raise FileNotFoundError
                with open("prompts/dashboard_prompt.txt", "r") as f:
                    base_prompt = f.read().format(schema_info=schema, user_query=user_input)
                response = self.model.generate_content([base_prompt])
                text = response.text.replace('```json', '').replace('```', '').strip()
                parsed = json.loads(text)
                if 'sql' in parsed:
                    return parsed
            except Exception:
                # fallback to local parser if remote fails
                pass

        return self._fallback_plan(user_input, schema)

    def _fallback_plan(self, user_input, schema):
        text = user_input.strip().lower()
        if text.startswith(('select', 'with', 'show', 'describe')):
            # rely on direct SQL query
            return {'sql': user_input, 'chart_type': 'table', 'x': None, 'y': None}

        # fallback automatic selection of table
        table = None
        for t in schema:
            if t.lower() in text:
                table = t
                break
        if table is None and len(schema) > 0:
            table = list(schema.keys())[0]

        sql = f"SELECT * FROM '{table}' LIMIT 100" if table else ""

        chart_type = 'table'
        x = None
        y = None
        if table and schema.get(table):
            numeric_columns = [c for c in schema.get(table) if c not in ['id', 'name', 'date', 'category']]
            if len(numeric_columns) >= 1:
                x = schema[table][0]
                y = numeric_columns[0]
                chart_type = 'bar'

        return {'sql': sql, 'chart_type': chart_type, 'x': x, 'y': y}

    def get_insight(self, data_summary):
        if self.use_remote:
            prompt = f"As a business analyst, provide a 2-sentence key insight from this data: {data_summary}"
            try:
                return self.model.generate_content(prompt).text
            except Exception:
                pass

        # Local insight fallback:
        if not data_summary:
            return "No data to analyze."

        # simple data summary insight with heuristics
        lines = data_summary.splitlines()
        n = min(3, len(lines))
        return f"Preview of data (first {n} rows) is shown. The model recommends inspecting trends and outliers in numeric columns. "
