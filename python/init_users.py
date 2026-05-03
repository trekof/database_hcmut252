#!/usr/bin/env python3
"""
Replace inline user creation with SQL file execution.
This script executes `sql/07_init_users.sql` to initialize demo users.
"""

import os
import sys
from pathlib import Path

from db import get_mysql_conn

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_FILE = BASE_DIR / 'sql' / '07_init_users.sql'

def run_sql_file(path):
    try:
        conn = get_mysql_conn()
        cur = conn.cursor()
        with open(path, 'r', encoding='utf-8') as f:
            sql = f.read()
        # Execute statements
        for stmt in sql.split(';'):
            s = stmt.strip()
            if s:
                cur.execute(s)
        conn.commit()
        cur.close()
        conn.close()
        print(f"✓ Executed {path}")
        return True
    except Exception as e:
        print(f"✗ Error executing {path}: {e}")
        return False


if __name__ == '__main__':
    print("🚀 Initializing demo users from SQL file")
    if not SQL_FILE.exists():
        print(f"✗ SQL file not found: {SQL_FILE}")
        sys.exit(1)
    ok = run_sql_file(SQL_FILE)
    sys.exit(0 if ok else 1)
