"""
Tkinter 메뉴얼 : https://docs.python.org/3/library/tkinter.html
tkinter: Tkinter 라이브러리를 사용해 화면창 구현
ttk: Tkinter에서 제공하는 스타일 위젯을 사용
filedialog: 파일 선택 대화 상자를 제공 (사진 첨부 기능에 사용)
"""
import tkinter as tk
from tkinter import filedialog
import os
from src.insert_diary import insert_diary
from src.read_all_diaries import read_all_diaries
from src.read_diary_by_date import read_diary_by_date
from src.update_diary import update_diary
from src.delete_diary import delete_diary

def create_main_window():
    # 메인 창 생성
    root = tk.Tk() # Tkinter의 메인 창
    root.title("Diary Application") # 창의 제목을 "Diary Application"으로 설정
    root.geometry("800x600") # 창의 크기를 가로 800, 세로 600 픽셀로 설정

    # 결과 출력 텍스트 창
    result_text = tk.Text(root, width=80, height=15) # 텍스트 입력 창
    result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5) # 레이아웃에 배치

    # 작업 후에도 입력 필드에 이전 값이 남는 문제 해결
    def clear_fields():
        id_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        date_entry.delete(0, tk.END)

    # 결과 출력창 초기화 함수
    def clear_result_text():
        result_text.delete("1.0", tk.END)

    # CRUD 기능 함수
    def handle_insert():
        title = title_entry.get() # 제목을 가져옴
        content = content_text.get("1.0", tk.END).strip() # 공백 제거
        photo_filename = filedialog.askopenfilename() # 파일 선택 상자
        date = date_entry.get()

        if not title or not date:
            result_text.insert(tk.END, "제목과 날짜는 필수 입력 항목입니다.\n")
            return

        # 사진 경로 유효성 검사
        if photo_filename and not os.path.isfile(photo_filename):
            result_text.insert(tk.END, "사진 파일이 존재하지 않습니다.\n")
            return

        try:
            insert_diary(title, content, photo_filename, date)
            result_text.insert(tk.END, "새 일기가 성공적으로 추가되었습니다!\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 추가 중 오류 발생: {e}\n")

    def handle_read_all():
        clear_result_text() # 기존 내용을 삭제
        try:
            result = read_all_diaries()  # 모든 일기 가져오는 함수 호출
            result_text.insert(tk.END, result + "\n")
        except Exception as e:
            result_text.insert(tk.END, f"전체 일기 조회 중 오류 발생: {e}\n")

    def handle_read_by_date():
        date = date_entry.get() # 날짜 입력 값을 가져옴
        if not date:
            result_text.insert(tk.END, "날짜를 입력해주세요.\n")
            return

        clear_result_text()
        try:
            result = read_diary_by_date(date)  # 특정 날짜 일기 가져오는 함수 호출
            result_text.insert(tk.END, result + "\n")
        except Exception as e:
            result_text.insert(tk.END, f"날짜별 조회 중 오류 발생: {e}\n")

    def handle_update():
        diary_id = id_entry.get() # 수정할 일기의 id
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        new_date = date_entry.get()

        if not diary_id or not diary_id.isdigit():
            result_text.insert(tk.END, "수정할 ID를 정확히 입력해주세요.\n")
            return

        if not new_title and not new_content and not new_date:
            result_text.insert(tk.END, "수정할 데이터를 입력해주세요.\n")
            return

        try:
            result = update_diary(diary_id, new_title, new_content, None, new_date)
            result_text.insert(tk.END, result + "\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 수정 중 오류 발생: {e}\n")

    def handle_delete():
        diary_id = id_entry.get()
        if not diary_id or not diary_id.isdigit():  # 숫자인지 확인
            result_text.insert(tk.END, "삭제할 ID를 정확히 입력해주세요.\n")
            return

        try:
            result = delete_diary(int(diary_id))  # 특정 ID에 해당하는 일기를 삭제
            result_text.insert(tk.END, result + "\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 삭제 중 오류 발생: {e}\n")

    # UI 구성 요소
    # label 텍스트를 표시
    # Entry 단일 라인의 텍스트 입력
    # button 버튼을 생성
    tk.Label(root, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(root, width=10)
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(root, text="제목:").grid(row=1, column=0, padx=5, pady=5)
    title_entry = tk.Entry(root, width=50)
    title_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="내용:").grid(row=2, column=0, padx=5, pady=5)
    content_text = tk.Text(root, width=50, height=5)
    content_text.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="날짜:").grid(row=3, column=0, padx=5, pady=5)
    date_entry = tk.Entry(root, width=20)
    date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Button(root, text="새 일기 작성", command=handle_insert).grid(row=4, column=0, padx=5, pady=5)
    tk.Button(root, text="전체 일기 조회", command=handle_read_all).grid(row=4, column=1, padx=5, pady=5, sticky="w")
    tk.Button(root, text="특정 날짜 조회", command=handle_read_by_date).grid(row=5, column=0, padx=5, pady=5)
    tk.Button(root, text="수정", command=handle_update).grid(row=5, column=1, padx=5, pady=5, sticky="w")
    tk.Button(root, text="삭제", command=handle_delete).grid(row=6, column=0, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
