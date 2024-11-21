# CRUD 기능 구현
'''
Create: 새로운 일기 추가
* Read: 저장된 일기를 조회
Update: 기존 일기를 수정
Delete: 일기를 삭제
'''
import sqlite3
from tabulate import tabulate
from src.database_connection import get_db_connection

def read_diary_by_date(date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 특정 날짜의 일기 조회 하기
        select_query = "SELECT * FROM diary WHERE date = ?;"
        cursor.execute(select_query, (date,))
        rows = cursor.fetchall()

        # 일기 출력
        if rows:
            headers = ["ID", "Title", "Content", "Photo Path", "Date"]
            return tabulate(rows, headers=headers, tablefmt="grid")
        else:
            print(f"{date}에 저장된 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기를 조회 중에 오류 발생: {e}")
    finally:
        if conn:  # conn이 None이 아닌 경우에만 close 호출
            conn.close()

# # 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    # 특정 날짜 조회
    read_diary_by_date("2024-11-20")
