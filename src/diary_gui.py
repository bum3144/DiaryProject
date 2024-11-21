import tkinter as tk
from tkinter import ttk, filedialog

def create_main_window():
    # 메인 화면 만들기 코드
    root = tk.Tk()
    root.title("Diary Application")
    root.geometry("800x600")

    # 새 일기 작성하기 버튼 코드
    tk.Label(root, text="제목:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(root, width=50)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="내용:").grid(row=1, column=0, padx=5, pady=5)
    content_text = tk.Text(root, width=50, height=5)
    content_text.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="사진:").grid(row=2, column=0, padx=5, pady=5)
    photo_button = tk.Button(root, text="사진 선택", command=lambda: filedialog.askopenfilename())
    photo_button.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    tk.Label(root, text="날짜:").grid(row=3, column=0, padx=5, pady=5)
    date_entry = tk.Entry(root, width=20)
    date_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    tk.Button(root, text="새 일기 작성", command=lambda: print("새 일기 작성")).grid(row=4, column=1, sticky="e", padx=5, pady=10)

    # 저장되 있는 일기 조회 버튼
    tk.Button(root, text="전체 일기 조회", command=lambda: print("전체 일기 조회")).grid(row=5, column=0, padx=5, pady=5)
    tk.Button(root, text="특정 날짜 조회", command=lambda: print("특정 날짜 조회")).grid(row=5, column=1, sticky="w", padx=5, pady=5)

    # 저장되 있는 일기 수정 및 삭제 버튼
    tk.Button(root, text="수정", command=lambda: print("수정")).grid(row=6, column=0, padx=5, pady=5)
    tk.Button(root, text="삭제", command=lambda: print("삭제")).grid(row=6, column=1, sticky="w", padx=5, pady=5)

    # 일기 조회 결과 출력
    result_text = tk.Text(root, width=80, height=15)
    result_text.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()
