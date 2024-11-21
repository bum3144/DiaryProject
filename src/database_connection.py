import os
import sqlite3

def get_db_connection():
    """
    루트 디렉토리의 diary.db에 연결
    """
    # 현재 파일(src/database_connection.py)의 절대 경로
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 프로젝트 루트 디렉토리 계산
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    # 루트 디렉토리의 diary.db 경로 설정
    db_path = os.path.join(root_dir, "diary.db")

    # SQLite 데이터베이스 연결
    return sqlite3.connect(db_path)
