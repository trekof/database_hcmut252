# python/db.py
import os
import sys
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")


def _mysql_host() -> str:
    """Chuẩn hóa host: trên Windows, 'localhost' hoặc '.' dùng named pipe và dễ lỗi 2017 — dùng TCP."""
    raw = os.getenv("MYSQL_HOST")
    h = (raw if raw is not None else "127.0.0.1").strip()
    if not h or h == ".":
        h = "127.0.0.1"
    if sys.platform == "win32" and h.lower() == "localhost":
        return "127.0.0.1"
    return h


MYSQL_CONFIG = {
    "host": _mysql_host(),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "database": os.getenv("MYSQL_DB"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD") or "",
    "autocommit": False,
}


def get_mysql_conn():
    """Tạo kết nối MySQL"""
    missing = []
    if not MYSQL_CONFIG.get("database"):
        missing.append("MYSQL_DB")
    if MYSQL_CONFIG.get("user") is None or str(MYSQL_CONFIG.get("user", "")).strip() == "":
        missing.append("MYSQL_USER")
    if missing:
        raise RuntimeError(
            "Thiếu biến môi trường: "
            + ", ".join(missing)
            + ". Tạo file .env ở thư mục gốc repo (cùng cấp README), ví dụ MYSQL_DB=btl2_db, MYSQL_USER=root, MYSQL_PASSWORD=..."
        )
    return mysql.connector.connect(**MYSQL_CONFIG)


def get_mysql_server_connection():
    """Kết nối tới server MySQL mà không chọn database (DROP/CREATE DATABASE)."""
    if MYSQL_CONFIG.get("user") is None or str(MYSQL_CONFIG.get("user", "")).strip() == "":
        raise RuntimeError(
            "Thiếu MYSQL_USER trong .env (đặt file .env ở thư mục gốc repo)."
        )
    return mysql.connector.connect(
        host=MYSQL_CONFIG["host"],
        port=MYSQL_CONFIG["port"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"],
        autocommit=True,
    )
