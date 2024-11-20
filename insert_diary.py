# CRUD 기능 구현
'''
Create: 새로운 일기 추가
Read: 저장된 일기를 조회
Update: 기존 일기를 수정
Delete: 일기를 삭제
'''
import sqlite3
import os

def insert_diary(title, content, photo_filename, date):
    try:
        # 이미지 저장할 images 폴더 경로
        image_folder = os.path.join(os.getcwd(), "images")
        os.makedirs(image_folder, exist_ok=True)  # 폴더가 없으면 생성하도록 한다.

        # 사진 파일이 저장될 경로를 설정
        photo_path = os.path.join(image_folder, photo_filename)

        # db 연결
        conn = sqlite3.connect("diary.db")
        cursor = conn.cursor()

        # SQL
        insert_query = """
        INSERT INTO diary (title, content, photo, date)
        VALUES (?, ?, ?, ?);
        """

        # 데이터 넣기
        cursor.execute(insert_query, (title, content, photo_path, date))
        conn.commit()
        print(f"새 일기가 추가되었습니다! 사진 경로: {photo_path}")
    except sqlite3.Error as e:
        print(f"데이터 입력 중 오류 발생: {e}")
    finally:
        conn.close()


# # 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    # 샘플 데이터 삽입
    insert_diary("나의 일기 TEST2", "나의 귀여운 강아지2를 또 소개합니다.", "./images/dog.jpg", "2024-11-20")
