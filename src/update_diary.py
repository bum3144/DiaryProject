# CRUD 기능 구현
'''
* Update: 기존 일기를 수정
'''
import sqlite3
import os
import datetime  # 타임스탬프 생성
from src.database_connection import get_db_connection

def update_diary(diary_id, title=None, content=None, photo=None, date=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 수정할 값을 동적으로 설정
        updates = []
        params = []

        if title:
            updates.append("title = ?")
            params.append(title)
        if content:
            updates.append("content = ?")
            params.append(content)
        if photo:
            # 이미지 저장 경로 처리
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_folder = os.path.join(project_root, "images")
            os.makedirs(image_folder, exist_ok=True)

            # 기존 파일 이름에서 이름과 확장자 분리
            file_basename, file_extension = os.path.splitext(os.path.basename(photo))
            # 타임스탬프 기반 고유 파일 이름 생성
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            unique_filename = f"{file_basename}_{timestamp}{file_extension}"
            dest_photo_path = os.path.join(image_folder, unique_filename)

            # 원본 사진 파일 복사
            source_photo_path = photo
            if os.path.exists(source_photo_path):
                with open(source_photo_path, "rb") as source, open(dest_photo_path, "wb") as destination:
                    destination.write(source.read())
                params.append(dest_photo_path)
                updates.append("photo = ?")  # photo 업데이트 쿼리에 추가
            else:
                return f"사진 파일이 존재하지 않습니다: {source_photo_path}"

        if date:
            updates.append("date = ?")
            params.append(date)

        # 업데이트 쿼리 생성
        if not updates:
            return "수정할 데이터가 없습니다."

        # 업데이트 쿼리
        updates_query = ", ".join(updates)
        sql_query = f"UPDATE diary SET {updates_query} WHERE id = ?;"
        params.append(diary_id)  # id는 항상 마지막에 추가

        # 업데이트 실행
        cursor.execute(sql_query, params)
        conn.commit()

        if cursor.rowcount > 0:
            return f"ID {diary_id}의 일기가 성공적으로 수정되었습니다."
        else:
            return f"ID {diary_id}에 해당하는 일기가 없습니다."

    except sqlite3.Error as e:
        return f"일기 수정 중 오류 발생: {e}"
    finally:
        if conn:  # conn이 None이 아닌 경우에만 close 호출
            conn.close()

# 테스트 실행
# 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    # 샘플 데이터 수정
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_photo_path = os.path.join(project_root, "dog.jpg")
    update_diary(
        diary_id=2,
        title="수정된 테스트 일기",
        content="타임스탬프 방식으로 이미지 이름이 생성됩니다.",
        photo=test_photo_path,
        date="2024-11-11"
    )
