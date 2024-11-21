"""
Tkinter 메뉴얼 : https://docs.python.org/3/library/tkinter.html
tkinter: Tkinter 라이브러리를 사용해 화면창 구현
ttk: Tkinter에서 제공하는 스타일 위젯을 사용
filedialog: 파일 선택 대화 상자를 제공 (사진 첨부 기능에 사용)
버튼 재배치: top_frame에 버튼들을 최상단에 배치, pack() 메서드를 사용하여 LEFT 방향으로 배치
"""
import tkinter as tk
import datetime
from tkinter import filedialog
from tkcalendar import Calendar
from src.insert_diary import insert_diary
from src.read_all_diaries import read_all_diaries
from src.read_diary_by_date import read_diary_by_date
from src.update_diary import update_diary
from src.delete_diary import delete_diary


def create_main_window():
    # 메인 창 생성
    root = tk.Tk()
    root.title("Diary Application")
    root.geometry("800x600")

    # 최상단 버튼 프레임 생성
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

    # 입력 필드와 결과 출력 프레임
    main_frame = tk.Frame(root)
    main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 버튼 함수 정의
    def handle_insert():
        title = title_entry.get()
        content = content_text.get("1.0", tk.END).strip()
        photo_filename = image_path_entry.get()
        date = date_entry.get()
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not title or not date:
            result_text.insert(tk.END, "제목과 날짜는 필수 입력 항목입니다.\n")
            return
        try:
            insert_diary(title, content, photo_filename, date)
            result_text.insert(tk.END, "새 일기가 성공적으로 추가되었습니다!\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 추가 중 오류 발생: {e}\n")

    def handle_read_all():
        try:
            clear_result_text()
            result = read_all_diaries()
            result_text.insert(tk.END, result + "\n")
        except Exception as e:
            result_text.insert(tk.END, f"전체 일기 조회 중 오류 발생: {e}\n")

    def handle_read_by_date():
        date = date_entry.get()
        if not date:
            result_text.insert(tk.END, "날짜를 입력해주세요.\n")
            return
        try:
            clear_result_text()
            result = read_diary_by_date(date)
            result_text.insert(tk.END, result + "\n")
        except Exception as e:
            result_text.insert(tk.END, f"날짜별 조회 중 오류 발생: {e}\n")

    def handle_update():
        diary_id = id_entry.get()
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        new_date = date_entry.get()
        if not diary_id or not diary_id.isdigit():
            result_text.insert(tk.END, "수정할 ID를 정확히 입력해주세요.\n")
            return
        try:
            update_diary(diary_id, new_title, new_content, None, new_date)
            result_text.insert(tk.END, f"ID {diary_id}의 일기가 수정되었습니다.\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 수정 중 오류 발생: {e}\n")

    def handle_delete():
        diary_id = id_entry.get()
        if not diary_id or not diary_id.isdigit():
            result_text.insert(tk.END, "삭제할 ID를 정확히 입력해주세요.\n")
            return
        try:
            delete_diary(int(diary_id))
            result_text.insert(tk.END, f"ID {diary_id}의 일기가 삭제되었습니다.\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 삭제 중 오류 발생: {e}\n")

    # 추가 유틸리티 함수
    def open_calendar():
        def select_date():
            date_entry.delete(0, tk.END)
            date_entry.insert(0, cal.get_date())
            calendar_window.destroy()

        calendar_window = tk.Toplevel(root)
        cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
        cal.pack(pady=10)
        select_button = tk.Button(calendar_window, text="선택", command=select_date)
        select_button.pack(pady=5)

    def select_image():
        photo_filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.gif")])
        image_path_entry.delete(0, tk.END)
        image_path_entry.insert(0, photo_filename)

    def clear_fields():
        id_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        content_text.delete("1.0", tk.END)
        date_entry.delete(0, tk.END)
        image_path_entry.delete(0, tk.END)

    def clear_result_text():
        result_text.delete("1.0", tk.END)

    # 버튼 추가
    tk.Button(top_frame, text="새 일기 작성", command=handle_insert).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="전체 일기 조회", command=handle_read_all).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="특정 날짜 조회", command=handle_read_by_date).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="수정", command=handle_update).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="삭제", command=handle_delete).pack(side=tk.LEFT, padx=5, pady=5)

    # 입력 필드 구성
    tk.Label(main_frame, text="ID:").grid(row=0, column=0, padx=5, pady=5)
    id_entry = tk.Entry(main_frame, width=10, state="readonly")
    id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(main_frame, text="제목:").grid(row=1, column=0, padx=5, pady=5)
    title_entry = tk.Entry(main_frame, width=60)
    title_entry.grid(row=1, column=1, padx=5, pady=5)

    # tk.Label(main_frame, text="내용:").grid(row=2, column=0, padx=5, pady=5)
    # content_text = tk.Text(main_frame, width=50, height=5)
    # content_text.grid(row=2, column=1, padx=5, pady=5)

    # 내용 필드에 스크롤바 추가
    tk.Label(main_frame, text="내용:").grid(row=2, column=0, padx=5, pady=5)
    # Frame 생성 (Text와 Scrollbar를 함께 배치)
    content_frame = tk.Frame(main_frame)
    content_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    # Text 위젯
    content_text = tk.Text(content_frame, width=60, height=10, wrap="word")  # wrap="word"로 줄 단위로 줄바꿈
    content_text.pack(side="left", fill="both", expand=True)
    # Scrollbar 위젯
    content_scrollbar = tk.Scrollbar(content_frame, command=content_text.yview)
    content_scrollbar.pack(side="right", fill="y")

    # Text와 Scrollbar 연결
    content_text.config(yscrollcommand=content_scrollbar.set)

    tk.Label(main_frame, text="날짜:").grid(row=3, column=0, padx=5, pady=5)
    date_entry = tk.Entry(main_frame, width=20)
    date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w") # Entry 위젯 클릭 시 달력 열기 함수 실행
    date_entry.bind("<Button-1>", lambda event: open_calendar()) # 클릭 이벤트와 open_calendar 함수 연결
    tk.Button(main_frame, text="날짜 선택", command=open_calendar).grid(row=3, column=2, padx=5, pady=5)

    tk.Label(main_frame, text="이미지 경로:").grid(row=4, column=0, padx=5, pady=5)
    # 이미지 경로 Entry (클릭 시 select_image 실행)
    image_path_entry = tk.Entry(main_frame, width=50)
    image_path_entry.grid(row=4, column=1, padx=5, pady=5)
    # Entry 위젯 클릭 시 이미지 선택 함수 실행
    image_path_entry.bind("<Button-1>", lambda event: select_image())  # 클릭 이벤트와 select_image 함수 연결
    tk.Button(main_frame, text="이미지 찾기", command=select_image).grid(row=4, column=2, padx=5, pady=5)

    # 결과 출력 텍스트 창
    result_text = tk.Text(main_frame, width=100, height=15)
    result_text.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
