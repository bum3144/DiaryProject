# CRUD 기능 구현
'''
Create: 새로운 일기 추가
Read: 저장된 일기를 조회
Update: 기존 일기를 수정
Delete: 일기를 삭제
'''
import sqlite3

def insert_diary(title, content, photo, date):
    try:
        # db 연결
        conn = sqlite3.connect("diary.db")
        cursor = conn.cursor()

        # SQL
        insert_query = """
        INSERT INTO diary (title, content, photo, date)
        VALUES (?, ?, ?, ?);
        """
        # 데이터 넣기
        cursor.execute(insert_query, (title, content, photo, date))
        conn.commit()
        print("새 일기가 추가되었습니다!")
    except sqlite3.Error as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
    finally:
        conn.close()

'''
# 테스트
if __name__ == "__main__":
    # 샘플 데이터 삽입
    insert_diary("첫 번째 일기 TEST", "나의 귀여운 강아지를 소개합니다.", "./tests/dog.jpg", "2024-11-20")
'''