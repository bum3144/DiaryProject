import sqlite3
from src.database_connection import get_db_connection

def read_diary_by_id(diary_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT id, title, content, photo, date FROM diary WHERE id = ?;"
        cursor.execute(query, (diary_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "title": row[1],
                "content": row[2],
                "photo": row[3],
                "date": row[4]
            }
        else:
            return None
    except sqlite3.Error as e:
        print(f"데이터 조회 중 오류 발생: {e}")
        return None
    finally:
        conn.close()
