import pandas as pd
import sqlite3
import os

class QueryExecutor:
    def __init__(self, db_path="data/business.db"):
        self.db_path = db_path
        data_dir = os.path.dirname(db_path) or 'data'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def sync_db(self):
        conn = sqlite3.connect(self.db_path)
        schema_parts = []
        for file in os.listdir('data'):
            if file.endswith('.csv'):
                table_name = file.replace('.csv', '')
                df = pd.read_csv(f"data/{file}")
                df.columns = [c.replace(' ', '_').lower() for c in df.columns]
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                schema_parts.append(f"Table '{table_name}' columns: {list(df.columns)}")
        conn.close()
        return " | ".join(schema_parts)

    def get_schema(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [x[0] for x in cursor.fetchall()]
        schema = {}
        for t in tables:
            cursor.execute(f"PRAGMA table_info('{t}')")
            cols = [c[1] for c in cursor.fetchall()]
            schema[t] = cols
        conn.close()
        return schema

    def run_sql(self, sql):
        conn = sqlite3.connect(self.db_path)
        try:
            return pd.read_sql_query(sql, conn)
        finally:
            conn.close()