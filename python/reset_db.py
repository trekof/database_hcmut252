# python/reset_db.py
"""
Script to drop and recreate the database
Useful for resetting your database to a clean state
"""

import sys
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "autocommit": True  # For DDL operations
}

def reset_database():
    """Drop and recreate the database"""
    db_name = os.getenv("MYSQL_DB")
    
    try:
        # Connect to MySQL (without selecting database)
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cur = conn.cursor()
        
        print(f"🔄 Resetting database '{db_name}'...")
        print()
        
        # Drop database if exists
        print(f"⏳ Dropping database '{db_name}'...")
        cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"✓ Dropped database '{db_name}'")
        
        # Create new database
        print(f"⏳ Creating new database '{db_name}'...")
        cur.execute(f"CREATE DATABASE {db_name}")
        print(f"✓ Created new database '{db_name}'")
        
        print()
        print("✅ Database reset complete!")
        print()
        print("Next steps:")
        print("  1. Run: python setup_db.py")
        print("  2. Or run: python demo_query.py")
        
        cur.close()
        conn.close()
        
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE RESET TOOL")
    print("=" * 60)
    print()
    
    # Confirm before resetting
    db_name = os.getenv("MYSQL_DB")
    response = input(f"⚠️  Are you sure you want to DROP '{db_name}'? (yes/no): ").strip().lower()
    
    if response == "yes":
        success = reset_database()
        sys.exit(0 if success else 1)
    else:
        print("❌ Reset cancelled")
        sys.exit(0)
