import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional

class SQLiteTool:
    def __init__(self, db_path: str = "data/northwind.sqlite"):
        self.db_path = db_path

    def get_schema(self, table_names: Optional[List[str]] = None) -> str:
        """Returns the schema for specified tables or all tables if None."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if table_names is None:
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' OR type='view';")
            table_names = [row[0] for row in cursor.fetchall()]
            
        schema_str = ""
        for table in table_names:
            cursor.execute(f"PRAGMA table_info('{table}')")
            columns = cursor.fetchall()
            if columns:
                schema_str += f"Table: {table}\n"
                for col in columns:
                    # cid, name, type, notnull, dflt_value, pk
                    schema_str += f"  - {col[1]} ({col[2]})\n"
                schema_str += "\n"
                
        conn.close()
        return schema_str

    def execute_sql(self, sql: str) -> Dict[str, Any]:
        """Executes a SQL query and returns the results or error."""
        conn = sqlite3.connect(self.db_path)
        try:
            # Use pandas for easy dataframe creation
            df = pd.read_sql_query(sql, conn)
            return {
                "columns": list(df.columns),
                "rows": df.to_dict(orient="records"),
                "error": None
            }
        except Exception as e:
            return {
                "columns": [],
                "rows": [],
                "error": str(e)
            }
        finally:
            conn.close()

    def get_tables(self) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' OR type='view';")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
