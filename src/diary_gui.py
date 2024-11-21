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

    # def handle_read_all():
    #     try:
    #         clear_result_text()
    #         result = read_all_diaries()
    #         result_text.insert(tk.END, result + "\n")
    #     except Exception as e:
    #         result_text.insert(tk.END, f"전체 일기 조회 중 오류 발생: {e}\n")

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
        # diary_id = id_entry.get()
        # 일기 수정 시 ID는 내부적으로 관리
        diary_id = None  # 내부적으로 선택된 ID를 가져오는 로직 필요
        new_title = title_entry.get()
        new_content = content_text.get("1.0", tk.END).strip()
        new_date = date_entry.get()

        if not diary_id:
            result_text.insert(tk.END, "수정할 일기를 선택해주세요.\n")
            return

        if not new_title and not new_content and not new_date:
            result_text.insert(tk.END, "수정할 일기를 입력해주세요.\n")
            return

        try:
            update_diary(diary_id, new_title, new_content, None, new_date)
            result_text.insert(tk.END, f"ID {diary_id}의 일기가 수정되었습니다.\n")
            clear_fields()
        except Exception as e:
            result_text.insert(tk.END, f"일기 수정 중 오류 발생: {e}\n")

    # def handle_delete():
    #     diary_id = id_entry.get()
    #     if not diary_id or not diary_id.isdigit():
    #         result_text.insert(tk.END, "삭제할 ID를 정확히 입력해주세요.\n")
    #         return
    #     try:
    #         delete_diary(int(diary_id))
    #         result_text.insert(tk.END, f"ID {diary_id}의 일기가 삭제되었습니다.\n")
    #         clear_fields()
    #     except Exception as e:
    #         result_text.insert(tk.END, f"일기 삭제 중 오류 발생: {e}\n")
    def handle_delete():
        def open_delete_selection():
            # 삭제할 ID를 선택하는 새로운 창 생성
            selection_window = tk.Toplevel(root)
            selection_window.title("삭제할 일기 선택")
            selection_window.geometry("400x300")

            try:
                # 저장된 일기 데이터 조회
                diaries = read_all_diaries()
                if not diaries:  # 반환값이 빈 리스트일 경우 처리
                    tk.Label(selection_window, text="삭제할 일기가 없습니다.").pack()
                    return

                # 데이터 출력 및 삭제 버튼 생성
                for diary in diaries:
                    if len(diary) == 5:  # 데이터가 올바른지 확인 (5개 필드: ID, 제목, 내용, 사진, 날짜)
                        diary_id, diary_title, _, _, diary_date = diary
                        diary_summary = f"ID: {diary_id}, 제목: {diary_title}, 날짜: {diary_date}"
                        tk.Button(
                            selection_window,
                            text=diary_summary,
                            command=lambda id=diary_id: [delete_diary(id), selection_window.destroy()]
                        ).pack(fill=tk.X, pady=2)
                    else:
                        # 데이터 손상 시 메시지 표시
                        tk.Label(selection_window, text="일기 데이터가 손상되었습니다.").pack()
            except Exception as e:
                tk.Label(selection_window, text=f"일기 조회 중 오류 발생: {e}").pack()

        # 삭제 창 열기
        open_delete_selection()

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

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
