# python/db.py
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "database": os.getenv("MYSQL_DB"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "autocommit": False
}

def get_mysql_conn():
    """Tạo kết nối MySQL"""
    return mysql.connector.connect(**MYSQL_CONFIG)
