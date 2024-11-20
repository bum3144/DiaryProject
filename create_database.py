import sqlite3

# 데이터베이스 diary.db 파일을 생성하고 연결
conn = sqlite3.connect("diary.db")

# 커서 객체 생성 - SQL 문을 실행하는 데 사용
cursor = conn.cursor()

print("Database created and connected successfully!")

# 데이터베이스 작업이 끝난 후 연결을 종료
conn.close()