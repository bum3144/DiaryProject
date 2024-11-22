# CRUD 기능 구현
'''
* Create: 새로운 일기 추가
Read: 저장된 일기를 조회
Update: 기존 일기를 수정
Delete: 일기를 삭제
'''
import sqlite3
import os
import datetime  # 타임스탬프 생성에 사용

def insert_diary(title, content, photo_filename, date):
    conn = None  # conn 변수를 초기화
    try:
        # 이미지 저장할 images 폴더 경로
        # 루트 디렉토리 기준으로 images 폴더 경로 설정
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # src 상위 디렉토리
        image_folder = os.path.join(project_root, "images")
        os.makedirs(image_folder, exist_ok=True)  # 폴더가 없으면 생성하도록 한다.

        # # 사진 파일이 저장될 경로를 설정
        # photo_path = os.path.join(image_folder, photo_filename)

        # 이미지 경로 처리
        if photo_filename and os.path.exists(photo_filename):
            # 타임스탬프를 추가한 유니크한 파일 이름 생성
            file_basename, file_extension = os.path.splitext(os.path.basename(photo_filename))
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{file_basename}_{timestamp}{file_extension}"
            dest_photo_path = os.path.join(image_folder, unique_filename)

            # 이미지 파일 복사
            with open(photo_filename, "rb") as source, open(dest_photo_path, "wb") as destination:
                destination.write(source.read())
        else:
            # 이미지를 선택하지 않았을 경우 경로를 빈 문자열로 설정
            dest_photo_path = ""

        # db 연결
        conn = sqlite3.connect(os.path.join(project_root, "diary.db"))
        cursor = conn.cursor()

        # 마지막 ID를 조회하여 다음 ID 설정
        cursor.execute("SELECT MAX(id) FROM diary;")
        last_id = cursor.fetchone()[0] or 0  # None일 경우 0으로 처리
        next_id = last_id + 1

        # SQL
        insert_query = """
        INSERT INTO diary (title, content, photo, date)
        VALUES (?, ?, ?, ?);
        """

        # 데이터 넣기
        cursor.execute(insert_query, (title, content, dest_photo_path, date))
        conn.commit()
        print(f"새 일기가 추가되었습니다! 사진 경로: {dest_photo_path}")
    except sqlite3.Error as e:
        print(f"데이터 입력 중 오류 발생: {e}")
    finally:
        # conn이 존재할 경우에만 닫기
        if conn:
            conn.close()


