import sqlite3

def read_all_diaries():
    try:
        conn = sqlite3.connect("diary.db")
        cursor = conn.cursor()

        # 모든 글 조회하는 쿼리
        select_query = "SELECT * FROM diary;"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # 글 출력
        if rows:
            print("저장된 일기 목록:")
            for row in rows:
                print(f"ID: {row[0]}, 제목: {row[1]}, 내용: {row[2]}, 사진 경로: {row[3]}, 날짜: {row[4]}")
        else:
            print("저장된 일기가 없습니다.")

    except sqlite3.Error as e:
        print(f"일기를 조회 중 오류가 발생.: {e}")
    finally:
        conn.close()

# 테스트 실행
if __name__ == "__main__":
    read_all_diaries()
