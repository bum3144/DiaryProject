# CRUD 기능 구현
'''
Create: 새로운 일기 추가
Read: 저장된 일기를 조회
Update: 기존 일기를 수정
* Delete: 일기를 삭제
'''
import sqlite3
from src.database_connection import get_db_connection

# 특정 ID의 데이터를 삭제
def delete_diary(diary_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 삭제 전 확인 후 삭제하도록 처리
        confirm = input(f"ID {diary_id}의 일기를 삭제하시겠습니까? (y/n): ")
        if confirm.lower() != "y":
            print("삭제 작업이 취소되었습니다.")
            return

        # 일기 삭제 쿼리
        delete_query = "DELETE FROM diary WHERE id = ?;"
        cursor.execute(delete_query, (diary_id,))
        conn.commit()

        # 일기 삭제 확인
        if cursor.rowcount > 0:
            print(f"ID {diary_id}의 일기가 삭제되었습니다!")
        else:
            print(f"ID {diary_id}에 해당하는 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기 삭제 중 오류 발생: {e}")
    finally:
        if conn:  # conn이 None이 아닌 경우에만 close 호출
            conn.close()

# 날짜별로 데이터를 삭제
def delete_diaries_by_date(date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 삭제 전 확인
        confirm = input(f"{date}의 모든 일기를 삭제하시겠습니까? (y/n): ")
        if confirm.lower() != "y":
            print("삭제 작업이 취소되었습니다.")
            return

        # 날짜별 삭제 쿼리
        delete_query = "DELETE FROM diary WHERE date = ?;"
        cursor.execute(delete_query, (date,))
        conn.commit()

        # 삭제 확인
        if cursor.rowcount > 0:
            print(f"{date}에 해당하는 모든 일기가 삭제되었습니다!")
        else:
            print(f"{date}에 해당하는 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기 삭제 중 오류 발생: {e}")
    finally:
        if conn:  # conn이 None이 아닌 경우에만 close 호출
            conn.close()




# 테스트 실행
# 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.

if __name__ == "__main__":
    # 삭제 테스트
    delete_diary(3)  # 삭제하려는 ID를 지정

# if __name__ == "__main__":
#     # 특정 날짜 일기 삭제 테스트
#     delete_diaries_by_date("2024-11-19")