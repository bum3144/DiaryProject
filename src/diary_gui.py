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
from tkinter import messagebox  # 경고 창을 위한 모듈
from tkcalendar import Calendar
from src.insert_diary import insert_diary
from src.read_all_diaries import read_all_diaries
from src.read_diary_by_date import read_diary_by_date
from src.update_diary import update_diary
from src.delete_diary import delete_diary
from src.read_diary_by_id import read_diary_by_id


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

    # 초기화 함수
    def clear_fields():
        id_entry.config(state="normal")  # ID 필드 잠금 해제
        id_entry.delete(0, tk.END)  # ID 필드 내용 삭제
        id_entry.config(state="readonly")  # 다시 읽기 전용으로 설정

        title_entry.delete(0, tk.END)  # 제목 필드 초기화
        content_text.delete("1.0", tk.END)  # 내용 필드 초기화
        date_entry.delete(0, tk.END)  # 날짜 필드 초기화
        image_path_entry.delete(0, tk.END)  # 이미지 경로 필드 초기화
        result_text.delete("1.0", tk.END)  # 결과 텍스트 창 초기화

    # 버튼 함수 정의
    def handle_insert():
        title = title_entry.get()
        content = content_text.get("1.0", tk.END).strip()
        photo_filename = image_path_entry.get()
        date = date_entry.get()
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        if not title or not date:
            result_text.insert(tk.END, f"제목과 내용은 필수 입력 항목입니다.(날짜 미입력시 오늘 날짜 자동저장)\n")
            return
        try:
            insert_diary(title, content, photo_filename, date)
            result_text.insert(tk.END, f"새 일기가 성공적으로 추가되었습니다!\n")

            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 추가 중 오류 발생: {e}\n")

    def handle_read_all():
        try:
            clear_result_text()
            diaries = read_all_diaries()
            if diaries:
                # 테이블 헤더 추가
                result_text.insert(tk.END, "=== 저장된 일기 목록 ===\n")
                result_text.insert(tk.END, f"{'ID':<15}{'제목':<55}{'날짜':<30}\n")
                result_text.insert(tk.END, "-" * 100 + "\n")  # 총 100글자의 구분선

                # 각 일기 데이터 출력
                for diary in diaries:
                    diary_id, title, _, _, date = diary
                    result_text.insert(tk.END, f"{diary_id:<15}{title[:53]:<55}{date:<30}\n")  # 제목은 53자로 자름
            else:
                result_text.insert(tk.END, "저장된 일기가 없습니다.\n")
        except Exception as e:
            result_text.insert(tk.END, f"전체 일기 조회 중 오류 발생: {e}\n")

    def handle_read_by_date():
        # 달력 창을 열어 날짜를 선택하게 함
        def open_calendar_for_search():
            def select_date():
                selected_date = cal.get_date()  # 달력에서 선택한 날짜를 가져옴
                clear_result_text()  # 기존 결과를 초기화
                try:
                    # 선택한 날짜로 조회
                    diaries = read_diary_by_date(selected_date)
                    if diaries and isinstance(diaries, list):  # 반환값이 리스트인지 확인
                        # 테이블 헤더 추가
                        result_text.insert(tk.END, f"=== {selected_date}의 저장된 일기 ===\n")
                        result_text.insert(tk.END, f"{'ID':<15}{'제목':<55}{'날짜':<30}\n")
                        result_text.insert(tk.END, "-" * 100 + "\n")  # 구분선

                        # 데이터 출력
                        for diary in diaries:
                            if len(diary) == 5:  # 데이터가 튜플 형식인지 확인
                                diary_id, title, _, _, date = diary
                                result_text.insert(tk.END, f"{diary_id:<15}{title[:53]:<55}{date:<30}\n")
                            else:
                                result_text.insert(tk.END, "잘못된 데이터 형식: {diary}\n")
                    else:
                        result_text.insert(tk.END, f"{selected_date}에 해당하는 일기가 없습니다.\n")
                except Exception as e:
                    result_text.insert(tk.END, f"날짜별 조회 중 오류 발생: {e}\n")
                calendar_window.destroy()  # 달력 창 닫기

            # 달력 창 생성
            calendar_window = tk.Toplevel(root)
            calendar_window.title("날짜 선택")
            cal = Calendar(calendar_window, selectmode="day", date_pattern="yyyy-mm-dd")
            cal.pack(pady=10)

            # 선택 버튼 생성
            select_button = tk.Button(calendar_window, text="선택", command=select_date)
            select_button.pack(pady=5)

        # 달력 창을 열도록 호출
        open_calendar_for_search()

    def handle_update():
        diary_id = id_entry.get()  # ID를 가져옴
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        new_date = date_entry.get()
        new_photo = image_path_entry.get()

        # ID 확인
        if not diary_id or not diary_id.isdigit():
            result_text.insert(tk.END, "조회 후 수정할 일기를 선택해 주세요.\n")
            return

        # 수정할 데이터 확인
        if not new_title and not new_content and not new_date:
            result_text.insert(tk.END, "수정할 데이터를 입력해주세요.\n")
            return

        # 경고 창 띄움
        confirm = messagebox.askyesno("수정 확인", f"ID {diary_id}의 일기를 수정하시겠습니까?")
        if confirm:  # "네" 선택 시
            try:
                # DB 업데이트 호출
                update_diary(int(diary_id), new_title, new_content, new_photo, new_date)
                result_text.insert(tk.END, f"ID {diary_id}의 일기가 성공적으로 수정되었습니다.\n")
                clear_fields()  # 입력 필드 초기화
                handle_read_all()  # 수정 후 전체 리스트 새로고침
            except Exception as e:
                result_text.insert(tk.END, f"일기 수정 중 오류 발생: {e}\n")
        else:  # "아니오" 선택 시
            result_text.insert(tk.END, "수정 작업이 취소되었습니다.\n")

    def handle_delete():
        # ID 필드에서 값을 가져옴
        diary_id = id_entry.get()

        # ID가 없거나 잘못된 값일 경우
        if not diary_id or not diary_id.isdigit():
            result_text.insert(tk.END, "조회 후 삭제할 일기를 선택해 주세요.\n")
            return

        # 경고 창을 띄움
        confirm = messagebox.askyesno("삭제 확인", f"ID {diary_id}의 일기를 삭제하시겠습니까?")
        if confirm:  # 사용자가 네 를 선택했을 경우
            try:
                delete_diary(int(diary_id))  # 삭제 함수 호출
                result_text.insert(tk.END, f"ID {diary_id}의 일기가 성공적으로 삭제되었습니다.\n")
                clear_fields()  # 입력 필드 초기화
                handle_read_all()  # 삭제 후 전체 리스트 새로고침
            except Exception as e:
                result_text.insert(tk.END, f"일기 삭제 중 오류 발생: {e}\n")
        else:
            result_text.insert(tk.END, "삭제 작업이 취소되었습니다.\n")  # 아니오 선택 시 메시지 출력

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

    # def clear_fields():
    #     id_entry.delete(0, tk.END)
    #     title_entry.delete(0, tk.END)
    #     content_text.delete("1.0", tk.END)
    #     date_entry.delete(0, tk.END)
    #     image_path_entry.delete(0, tk.END)

    def clear_result_text():
        result_text.delete("1.0", tk.END)

    def on_result_enter(event):
        result_text.config(cursor="hand2")  # hand2는 손가락 모양의 커서

    def on_result_leave(event):
        result_text.config(cursor="")  # 기본 커서로 복원
    def on_result_click(event):
        try:
            clicked_index = result_text.index(f"@{event.x},{event.y}")
            clicked_line = result_text.get(clicked_index + " linestart", clicked_index + " lineend").strip()

            # 테이블 헤더나 구분선 제외
            if clicked_line.startswith("ID") or clicked_line.startswith("=") or clicked_line.startswith("-"):
                return

            # 데이터 파싱
            diary_id = clicked_line[:15].strip()  # ID: 처음 15자
            title = clicked_line[15:70].strip()  # 제목: 15~70자
            date = clicked_line[70:].strip()  # 날짜: 70자 이후

            # 필드에 데이터 로드
            id_entry.config(state="normal")
            id_entry.delete(0, tk.END)
            id_entry.insert(0, diary_id)
            id_entry.config(state="readonly")

            title_entry.delete(0, tk.END)
            title_entry.insert(0, title)

            date_entry.delete(0, tk.END)
            date_entry.insert(0, date)

            # 내용 및 이미지 경로 로드
            diary_data = read_diary_by_id(int(diary_id))
            if diary_data:
                content_text.delete("1.0", tk.END)
                content_text.insert("1.0", diary_data['content'])

                image_path_entry.delete(0, tk.END)
                image_path_entry.insert(0, diary_data['photo'])
            else:
                result_text.insert(tk.END, "선택한 데이터의 세부 정보를 찾을 수 없습니다.\n")
        except Exception as e:
            result_text.insert(tk.END, f"데이터 파싱 중 오류 발생: {e}\n")

    # 버튼 추가
    tk.Button(top_frame, text="새 일기 저장", fg="green", command=handle_insert).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="전체 일기 조회", command=handle_read_all).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="특정 날짜 조회", command=handle_read_by_date).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="수정하기", fg="blue", command=handle_update).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(top_frame, text="삭제하기", fg="red", command=handle_delete).pack(side=tk.LEFT, padx=5, pady=5)
    # 취소 버튼 추가
    tk.Button(top_frame, text="취소하기", command=clear_fields).pack(side=tk.LEFT, padx=5, pady=5)

    # 입력 필드 구성
    # ID 입력 필드 제거 : ID는 시스템 내부적으로 사용되며, 사용자가 볼 필요가 없기에 비공개처리
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
    result_text.bind("<Button-1>", on_result_click) # 클릭 이벤트 처리
    result_text.bind("<Enter>", on_result_enter)  # 마우스가 위젯에 들어올 때 커서 변경
    result_text.bind("<Leave>", on_result_leave)  # 마우스가 위젯에서 나갈 때 커서 복원
    root.mainloop()


if __name__ == "__main__":
    create_main_window()
