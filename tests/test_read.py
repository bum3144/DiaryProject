import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # 상위 폴더 경로 추가

import sqlite3

def read_all_diaries():
    try:
        # 데이터베이스 연결
        conn = sqlite3.connect("../diary.db")  # 상위 폴더에 있는 DB 파일 참조
        cursor = conn.cursor()

        # 저장된 모든 데이터 조회
        select_query = "SELECT * FROM diary;"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        # 데이터 출력
        if rows:
            print("저장된 일기 목록:")
            for row in rows:
                print(f"ID: {row[0]}, 제목: {row[1]}, 내용: {row[2]}, 사진 경로: {row[3]}, 날짜: {row[4]}")
        else:
            print("저장된 데이터가 없습니다.")

    except sqlite3.Error as e:
        print(f"데이터 조회 중 오류 발생: {e}")
    finally:
        conn.close()

# 테스트 실행
if __name__ == "__main__":
    read_all_diaries()
