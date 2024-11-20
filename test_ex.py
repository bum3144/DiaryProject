'''
import sqlite3
# sqlite2 버전 확인
print(sqlite3.sqlite_version)

from PIL import Image
# Pillow 설치 확인
print("Pillow is working!")
'''

'''
# db 파일(diary.db)이 제대로 생성되고 접근 가능한지 확인
'''

import sqlite3
import os

# db 파일 경로
db_file = "diary.db"

'''
# db 파일 존재 여부 확인
if os.path.exists(db_file):
    print(f"'{db_file}' 파일이 존재합니다. db 확인을 시작합니다.")
else:
    print(f"'{db_file}' 파일이 없습니다. db 먼저 생성하세요.")
    exit()
'''

'''
# db 연결 테스트
try:
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    print("db에 연결 성공.")

    # SQLite 버전 확인
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()
    print(f"SQLite 버전: {version[0]}")
except sqlite3.Error as e:
    print(f"db 연결 실패: {e}")
finally:
    conn.close()
    print("db 연결 종료.")
'''