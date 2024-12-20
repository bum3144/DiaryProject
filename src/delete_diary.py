# CRUD 기능 구현
'''
* Delete: 일기를 삭제
'''
import sqlite3
import os
from src.database_connection import get_db_connection

# 특정 ID의 데이터를 삭제
def delete_diary(diary_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 삭제 전 해당 ID의 이미지 경로 조회
        select_query = "SELECT photo FROM diary WHERE id = ?;"
        cursor.execute(select_query, (diary_id,))
        row = cursor.fetchone()

        if row:
            photo_path = row[0]

            # 삭제 전 해당 ID의 이미지 경로 조회
            select_query = "SELECT photo FROM diary WHERE id = ?;"
            cursor.execute(select_query, (diary_id,))
            row = cursor.fetchone()

            if row:
                photo_path = row[0]

                # 이미지 파일 삭제
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                    image_message = f"이미지 파일이 삭제되었습니다: {photo_path}"
                else:
                    image_message = f"이미지 파일이 존재하지 않습니다: {photo_path}"

                # 데이터 삭제
                delete_query = "DELETE FROM diary WHERE id = ?;"
                cursor.execute(delete_query, (diary_id,))
                conn.commit()

                if cursor.rowcount > 0:
                    return f"ID {diary_id}의 일기가 삭제되었습니다!\n{image_message}"
                else:
                    return f"ID {diary_id}에 해당하는 일기가 없습니다."
            else:
                return f"ID {diary_id}에 해당하는 일기가 없습니다."

    except sqlite3.Error as e:
        return f"일기 삭제 중 오류 발생: {e}"

    finally:
        if conn:  # conn이 None이 아닌 경우에만 close 호출
            conn.close()


# 날짜별로 데이터를 삭제
def delete_diaries_by_date(date):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 삭제 전 해당 날짜의 이미지 경로 조회
        select_query = "SELECT photo FROM diary WHERE date = ?;"
        cursor.execute(select_query, (date,))
        rows = cursor.fetchall()

        if rows:
            image_messages = []
            for row in rows:
                photo_path = row[0]

                # 이미지 파일 삭제
                if os.path.exists(photo_path):
                    os.remove(photo_path)
                    image_messages.append(f"이미지 파일이 삭제되었습니다: {photo_path}")
                else:
                    image_messages.append(f"이미지 파일이 존재하지 않습니다: {photo_path}")

            # 데이터 삭제
            delete_query = "DELETE FROM diary WHERE date = ?;"
            cursor.execute(delete_query, (date,))
            conn.commit()

            if cursor.rowcount > 0:
                image_messages_str = "\n".join(image_messages)
                return f"{date}에 해당하는 모든 일기가 삭제되었습니다!\n{image_messages_str}"
            else:
                return f"{date}에 해당하는 모든 일기가 삭제되지 않았습니다."
        else:
            return f"{date}에 해당하는 일기가 없습니다."

    except sqlite3.Error as e:
        return f"일기 삭제 중 오류 발생: {e}"

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
    delete_diary(1)  # 삭제하려는 ID를 지정

# if __name__ == "__main__":
#     # 특정 날짜 일기 삭제 테스트
#     delete_diaries_by_date("2024-11-19")