# python/setup_db.py
import sys
from pathlib import Path

# Thêm path để import db.py
sys.path.insert(0, str(Path(__file__).parent))

from db import get_mysql_conn


def run_sql_file(path):
    """Chạy file SQL thường (table, data)"""
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()

        for stmt in sql.split(";"):
            stmt = stmt.strip()
            if stmt:
                cur.execute(stmt)

        conn.commit()
        print(f"✓ Executed {path}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error executing {path}: {e}")
    finally:
        cur.close()
        conn.close()


def run_routine_file(path):
    """Chạy file SQL có PROCEDURE/TRIGGER/FUNCTION"""
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            sql = f.read()

        # Split by CREATE PROCEDURE/TRIGGER/FUNCTION
        statements = []
        current_stmt = ""
        
        for line in sql.split("\n"):
            current_stmt += line + "\n"
            if line.strip().upper().endswith("END;"):
                statements.append(current_stmt.strip())
                current_stmt = ""
        
        # Execute each statement
        for stmt in statements:
            if stmt.strip() and not stmt.strip().startswith("--"):
                cur.execute(stmt)
        
        conn.commit()
        print(f"✓ Executed routine {path}")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error executing {path}: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Lấy đường dẫn thư mục SQL
    sql_dir = os.path.join(os.path.dirname(__file__), "..", "sql")
    
    print("🔧 Setting up database...")
    print()
    
    # Drop and recreate database
    try:
        conn = get_mysql_conn()
        cur = conn.cursor()
        db_name = os.getenv("MYSQL_DB")
        
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
        conn.commit()
        cur.close()
        conn.close()
        print(f"✓ Database {db_name} dropped and recreated")
        print()
    except Exception as e:
        print(f"⚠️  Warning: {e}")
        print()
    
    # Chạy các file theo thứ tự
    run_sql_file(os.path.join(sql_dir, "01_create_tables.sql"))
    run_sql_file(os.path.join(sql_dir, "02_constraints.sql"))
    run_sql_file(os.path.join(sql_dir, "03_sample_data.sql"))
    run_routine_file(os.path.join(sql_dir, "04_procedures.sql"))
    run_routine_file(os.path.join(sql_dir, "05_triggers.sql"))
    run_routine_file(os.path.join(sql_dir, "06_functions.sql"))
    run_sql_file(os.path.join(sql_dir, "07_init_users.sql"))
    
    print()
    print("✓ Database setup completed!")
