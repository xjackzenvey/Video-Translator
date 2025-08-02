import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time

from ..workflow import workflow


class TkinterInterface:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.title('视频翻译工具')
        
        # 禁用窗口大小调整
        self.root.resizable(False, False)
        
        self.rec_txt = ''
        self.translated_txt = ''
        
        # 第一行：选择文件
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = tk.Entry(top_frame, textvariable=self.file_path_var, width=50)
        self.file_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.select_btn = tk.Button(top_frame, text='选择文件', command=self.select_file)
        self.select_btn.pack(side=tk.RIGHT, padx=10)
        
        
        # 中间显示文本框
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=False)
        self.result_text = tk.Text(self.middle_frame, wrap=tk.WORD, state=tk.DISABLED, font=('微软雅黑', 15))
        self.result_text.pack(expand=True, fill=tk.BOTH)
        
        # 底部按钮
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(pady=10, padx=5, fill=tk.BOTH)
        
        self.start_btn = tk.Button(self.bottom_frame, text='开始翻译', command=self.start_task, width=20)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_rec_btn = tk.Button(self.bottom_frame, text='复制原文', command=lambda: self.root.clipboard_clear() or self.root.clipboard_append(self.rec_txt), width=20)
        self.copy_rec_btn.pack(side=tk.LEFT, padx=5)
        
        self.copy_trans_btn = tk.Button(self.bottom_frame, text='复制译文', command=lambda: self.root.clipboard_clear() or self.root.clipboard_append(self.translated_txt), width=20)
        self.copy_trans_btn.pack(side=tk.LEFT, padx=5)

        
        
    def select_file(self):
        file_path = filedialog.askopenfilename(title='选择视频文件', filetypes=[('视频文件', '*.mp4 *.avi *.mkv')])
        self.__clean_text_result()
        
        if file_path:
            self.file_path_var.set(file_path)
            
            
    def start_task(self):
        video_path = self.file_path_var.get()
        
        if not video_path:
            messagebox.ERROR('请先选择视频文件！')
        
        self.start_btn.config(state=tk.DISABLED)
        
        self.__clean_text_result()
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f'正在处理视频: {video_path}\n')
        self.result_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.run_detection, args=(video_path,))
        thread.start()
    
        
    def run_detection(self, video_path):
        rec_txt, translated_txt = workflow(video_path)
        self.root.after(0, self.update_result, rec_txt, translated_txt)
        
    
    def __clean_text_result(self):
        raw_state = self.result_text['state']
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=raw_state)
    
        
    def update_result(self, rec_txt, translated_txt):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"\n原文: {rec_txt}\n")
        self.result_text.insert(tk.END, f"翻译: {translated_txt}\n")
        self.result_text.config(state=tk.DISABLED)
        
        self.rec_txt = rec_txt
        self.translated_txt = translated_txt
        
        self.start_btn.config(state=tk.NORMAL)
        
    
    def show(self):
        self.root.mainloop()
        
        
if __name__ == "__main__":
    app = TkinterInterface()
    app.show()
        
        