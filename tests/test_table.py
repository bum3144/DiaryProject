# diary 테이블 생성 확인
import sqlite3

# db 연결
conn = sqlite3.connect("../diary.db")
cursor = conn.cursor()

# 테이블 목록 조회
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 테이블 목록 출력
if tables:
    print("테이블 목록:")
    for table in tables:
        print(f"- {table[0]}")
else:
    print("db에 테이블이 없습니다.")

# 연결 종료
conn.close()