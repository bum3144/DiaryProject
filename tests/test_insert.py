import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# test를 위해서 상위 폴더 경로 추가

from src.insert_diary import insert_diary
"""
 # TEST시에 insert_diary.py파일 수정하고 해야함  conn = sqlite3.connect("../diary.db")
"""
# 테스트 실행
if __name__ == "__main__":
    # 테스트 데이터
    title = "TEST폴더에서 일기 TEST"
    content = "이것은 테스트 테스트-나의 귀여운 강아지를 소개합니다"
    photo = "test_image.jpg"
    date = "2024-11-20"

    # insert_diary 함수 실행
    try:
        insert_diary(title, content, photo, date)
        print("테스트 성공: 데이터가 정상적으로 삽입되었습니다!")
    except Exception as e:
        print(f"테스트 실패: {e}")
