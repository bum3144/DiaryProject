# CRUD 기능 구현
'''
* Read: 저장된 일기를 조회
'''
import sqlite3
from src.database_connection import get_db_connection

def read_diary_by_date(date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT id, title, content, photo, date FROM diary WHERE date = ?;"
        cursor.execute(query, (date,))
        results = cursor.fetchall()
        # print("DEBUG: 조회된 데이터:", results)  # 반환값 출력
        return results
    except sqlite3.Error as e:
        print(f"데이터베이스 오류: {e}")
        return []
    finally:
        if conn:
            conn.close()

# # 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    # 특정 날짜 조회
    read_diary_by_date("2024-11-20")
