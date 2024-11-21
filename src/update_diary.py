# CRUD 기능 구현
'''
Create: 새로운 일기 추가
Read: 저장된 일기를 조회
* Update: 기존 일기를 수정
Delete: 일기를 삭제
'''
import sqlite3

def update_diary(diary_id, title=None, content=None, photo=None, date=None):
    try:
        conn = sqlite3.connect("diary.db")
        cursor = conn.cursor()

        # 수정
        updates = []
        params = []

        if title:
            updates.append("title = ?")
            params.append(title)
        if content:
            updates.append("content = ?")
            params.append(content)
        if photo:
            updates.append("photo = ?")
            params.append(photo)
        if date:
            updates.append("date = ?")
            params.append(date)

        # 업데이트 쿼리
        updates_query = ", ".join(updates)
        sql_query = f"UPDATE diary SET {updates_query} WHERE id = ?;"
        params.append(diary_id)

        # 업데이트 실행
        cursor.execute(sql_query, params)
        conn.commit()

        if cursor.rowcount > 0:
            print(f"ID {diary_id}의 일기가 수정되었습니다!")
        else:
            print(f"ID {diary_id}에 해당하는 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기 수정 중 오류 발생: {e}")
    finally:
        conn.close()

# 테스트 실행
# 테스트 코드
# 빠른 테스트를 위해 하단에 배치하여 개발 중 바로 바로 테스트 하기위해 유지
# 이 아래 내부의 코드는 독립 실행 시에만 작동하므로 안전하게 사용가능
# 다른 파일에서 이 코드를 import하여 사용할 때는 테스트 코드는 실행되지 않는다.
if __name__ == "__main__":
    # 샘플 데이터 수정
    update_diary(
        diary_id=1,
        title="수정된 테스트 일기",
        content="일기 내용이 수정되었습니다.",
        photo="./images/updated_dog.jpg",
        date="2024-11-21"
    )
