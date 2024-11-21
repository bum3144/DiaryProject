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
# pip install tabulate
# tabulate 라이브러리를 사용하여 표형식으로 출력

def read_all_diaries():
    try:
        conn = get_db_connection()  # 수정된 부분
        cursor = conn.cursor()

        # 모든 글 조회하는 쿼리
        select_query = "SELECT * FROM diary;"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # 글 출력
        if rows:
            headers = ["ID", "Title", "Content", "Photo Path", "Date"]
            shortened_rows = [
                (row[0], row[1], (row[2][:50] + '...') if len(row[2]) > 50 else row[2], row[3], row[4])
                for row in rows
            ]
            print(tabulate(shortened_rows, headers=headers, tablefmt="grid"))
        else:
            print("저장된 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기를 조회 중 오류가 발생.: {e}")
    finally:
        if conn: # conn이 None이 아닌 경우에만 close 호출
            conn.close()

# # 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    read_all_diaries()
