import sqlite3

conn = sqlite3.connect("diary.db")
cursor = conn.cursor()

# 테이블 만들기
create_table = """
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT,
    photo TEXT,
    date TEXT NOT NULL
);
"""
# 실행
cursor.execute(create_table)

print("테이블 'diary'를 성공적으로 생성했습니다.")

# 연결종류
conn.close()