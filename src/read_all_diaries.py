# CRUD 기능 구현
'''
* Read: 저장된 일기를 조회
'''
import sqlite3
from src.database_connection import get_db_connection

# read_all_diaries 함수에서 반환값 디버깅 추가
def read_all_diaries():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 모든 다이어리 조회 쿼리
        select_query = "SELECT * FROM diary;"
        cursor.execute(select_query)
        rows = cursor.fetchall()  # 모든 데이터 가져오기

        # 디버깅: 반환값 출력
        # print("디버깅: rows =", rows)

        return rows
    except sqlite3.Error as e:
        print(f"데이터베이스 조회 중 오류 발생: {e}")
        return []  # 오류 발생 시 빈 리스트 반환
    finally:
        if conn:
            conn.close()

# # 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    read_all_diaries()
