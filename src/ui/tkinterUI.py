import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

# 假设 workflow 函数放在上级目录的 workflow.py 中
from ..workflow import workflow


class TkinterInterface:
    def __init__(self, root=None):
        # Use ttkbootstrap 
        self.root = ttk.Window(themename="cosmo", title="视频翻译工具", resizable=(False, False))
        self.rec_txt = ""
        self.translated_txt = ""

        # 窗口居中
        self.center_window(1000, 650)

        # ------------------ 顶部：文件选择 ------------------
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill=X)

        self.file_path_var = ttk.StringVar()
        ttk.Entry(top, textvariable=self.file_path_var, width=80).pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        ttk.Button(top, text="选择文件", command=self.select_file, bootstyle=PRIMARY).pack(side=LEFT)

        # ------------------ 中部：结果显示 ------------------
        mid = ttk.Frame(self.root, padding=10)
        mid.pack(fill=BOTH, expand=YES)

        self.result_text = ScrolledText(mid, state=DISABLED, font=("微软雅黑", 12), height=15, wrap=WORD)
        self.result_text.pack(fill=BOTH, expand=YES)

        # ------------------ 底部：按钮区 ------------------
        btm = ttk.Frame(self.root, padding=10)
        btm.pack(fill=X)

        self.start_btn = ttk.Button(btm, text="开始翻译", command=self.start_task, bootstyle=SUCCESS)
        self.start_btn.pack(side=LEFT, padx=5)

        self.copy_rec_btn = ttk.Button(btm, text="复制原文", command=self.copy_rec, bootstyle=SECONDARY)
        self.copy_rec_btn.pack(side=LEFT, padx=5)

        self.copy_trans_btn = ttk.Button(btm, text="复制译文", command=self.copy_trans, bootstyle=SECONDARY)
        self.copy_trans_btn.pack(side=LEFT, padx=5)

        ttk.Button(btm, text="清空结果", command=self.__clean_text_result, bootstyle=WARNING).pack(side=RIGHT)

    # ------------------ 业务方法 ------------------
    def center_window(self, width, height):
        """让窗口出现在屏幕中央"""
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def select_file(self):
        path = filedialog.askopenfilename(
            title="选择视频文件",
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov *.flv")]
        )
        if path:
            self.file_path_var.set(path)
            self.__clean_text_result()

    def start_task(self):
        video_path = self.file_path_var.get()
        if not video_path:
            messagebox.showerror("提示", "请先选择视频文件！")
            return

        self.start_btn.config(state=DISABLED)
        self.__clean_text_result()
        self.write_log(f"正在处理视频：{video_path}\n")
        threading.Thread(target=self.run_detection, args=(video_path,), daemon=True).start()

    def run_detection(self, video_path):
        try:
            rec_txt, translated_txt = workflow(video_path)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"处理失败：{e}"))
            self.root.after(0, lambda: self.start_btn.config(state=NORMAL))
            return
        self.root.after(0, self.update_result, rec_txt, translated_txt)

    def write_log(self, msg):
        self.result_text.text.config(state=NORMAL)
        self.result_text.insert(END, msg)
        self.result_text.see(END)
        self.result_text.text.config(state=DISABLED)

    def update_result(self, rec_txt, translated_txt):
        self.rec_txt = rec_txt
        self.translated_txt = translated_txt

        self.result_text.text.config(state=NORMAL)
        self.result_text.insert(END, f"\n【原文】\n{rec_txt}\n\n【译文】\n{translated_txt}\n")
        self.result_text.text.config(state=DISABLED)
        self.start_btn.config(state=NORMAL)

    def __clean_text_result(self):
        self.result_text.text.config(state=NORMAL)
        self.result_text.text.delete(1.0, END)
        self.result_text.text.config(state=DISABLED)
        return
        
    def copy_rec(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.rec_txt)
        messagebox.showinfo("提示", "原文已复制到剪贴板")

    def copy_trans(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.translated_txt)
        messagebox.showinfo("提示", "译文已复制到剪贴板")

    def show(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TkinterInterface()
    app.show()