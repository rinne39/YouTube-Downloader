import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
import customtkinter as ctk
from tkinter import filedialog, messagebox
import yt_dlp
import subprocess

FONT_FAMILY = ("Microsoft YaHei UI", "微软雅黑", "Arial")
TITLE_FONT  = (FONT_FAMILY, 15, "bold")
NORMAL_FONT = (FONT_FAMILY, 13)
SMALL_FONT  = (FONT_FAMILY, 11)
BUTTON_FONT = (FONT_FAMILY, 14, "bold")

THEME_BLUE  = ("#0066CC", "#3498db")
THEME_RED   = ("#dc3545", "#e74c3c")
THEME_GREEN = ("#28a745", "#2ecc71")
THEME_GOLD  = ("#A67C00", "#f1c40f")

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_exe = os.path.join(base_path, 'ffmpeg.exe')
    return ffmpeg_exe if os.path.exists(ffmpeg_exe) else 'ffmpeg'

class TaskUI(ctk.CTkFrame):
    def __init__(self, master, title, url, **kwargs):
        super().__init__(master, **kwargs)
        self.url = url
        self.title_label = ctk.CTkLabel(self, text=title, font=NORMAL_FONT, anchor="w")
        self.title_label.pack(fill="x", padx=15, pady=(10, 0))
        self.p_bar = ctk.CTkProgressBar(self, height=8)
        self.p_bar.pack(fill="x", padx=15, pady=10)
        self.p_bar.set(0)
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(0, 10))
        self.info_label = ctk.CTkLabel(info_frame, text="准备中", font=SMALL_FONT, text_color="gray")
        self.info_label.pack(side="left")
        self.status_label = ctk.CTkLabel(info_frame, text="等待开始", font=SMALL_FONT, text_color="gray")
        self.status_label.pack(side="right")

class VideoCheckBox(ctk.CTkCheckBox):
    def __init__(self, master, title, url, **kwargs):
        super().__init__(master, text=title, font=NORMAL_FONT, **kwargs)
        self.url = url

class ModernYoutubeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Downloader by Rinne")
        self.geometry("1300x940")
        self.download_path = ctk.StringVar(value=os.path.join(os.getcwd(), 'downloads'))
        self.res_var = ctk.StringVar(value="2160")
        self.scan_videos = ctk.BooleanVar(value=True)
        self.scan_shorts = ctk.BooleanVar(value=True)
        self.scan_streams = ctk.BooleanVar(value=True)
        self.scroll_items = {"videos": [], "shorts": [], "streams": []}
        self.task_widgets = {}
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=10)
        self.tab_scan = self.tabs.add("视频扫描")
        self.tab_tasks = self.tabs.add("下载管理")
        self.setup_scan_page()
        self.setup_tasks_page()
        self.setup_footer()

    def setup_scan_page(self):
        header = ctk.CTkFrame(self.tab_scan, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)
        self.url_input = ctk.CTkEntry(header, placeholder_text="此处粘贴YouTube主页链接", height=45, font=NORMAL_FONT)
        self.url_input.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(header, text="开始扫描", width=120, height=45, font=BUTTON_FONT, command=self.start_scan).pack(side="left")
        opt_f = ctk.CTkFrame(self.tab_scan, fg_color="transparent")
        opt_f.pack(fill="x", padx=10, pady=0)
        ctk.CTkLabel(opt_f, text="筛选:", font=SMALL_FONT).pack(side="left", padx=5)
        ctk.CTkCheckBox(opt_f, text="普通视频", variable=self.scan_videos, font=SMALL_FONT).pack(side="left", padx=10)
        ctk.CTkCheckBox(opt_f, text="短视频", variable=self.scan_shorts, font=SMALL_FONT).pack(side="left", padx=10)
        ctk.CTkCheckBox(opt_f, text="直播回放", variable=self.scan_streams, font=SMALL_FONT).pack(side="left", padx=10)
        body = ctk.CTkFrame(self.tab_scan, fg_color="transparent")
        body.pack(fill="both", expand=True, pady=10)
        config = [("videos", "普通视频", THEME_BLUE), ("shorts", "短视频", THEME_RED), ("streams", "直播回放", THEME_GREEN)]
        for i, (key, label, color) in enumerate(config):
            col = ctk.CTkFrame(body)
            col.place(relx=i*0.333 + 0.005, rely=0, relwidth=0.32, relheight=1)
            t_bar = ctk.CTkFrame(col, fg_color="transparent")
            t_bar.pack(fill="x", padx=5, pady=5)
            icon = ctk.CTkLabel(t_bar, text="", width=25)
            icon.pack(side="left")
            ctk.CTkLabel(t_bar, text=label, font=TITLE_FONT, text_color=color).pack(side="left", padx=5)
            ctk.CTkButton(t_bar, text="反选", width=40, height=22, font=SMALL_FONT, command=lambda k=key: self.toggle_inverse(k)).pack(side="right", padx=5)
            scroll = ctk.CTkScrollableFrame(col, fg_color=("gray88", "gray12"), corner_radius=0)
            scroll.pack(fill="both", expand=True, padx=2, pady=2)
            ctk.CTkButton(col, text=f"下载选中的{label}", height=35, font=SMALL_FONT, fg_color=color, command=lambda k=key: self.dl_selection(k)).pack(fill="x", padx=10, pady=10)
            self.scroll_items[key] = {"frame": scroll, "checkboxes": [], "icon_label": icon, "is_loading": False}

    def setup_tasks_page(self):
        self.task_scroll = ctk.CTkScrollableFrame(self.tab_tasks, fg_color="transparent")
        self.task_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        ctk.CTkButton(self.tab_tasks, text="清空完成项目", width=150, font=SMALL_FONT, command=self.clear_tasks).pack(pady=10)

    def setup_footer(self):
        footer = ctk.CTkFrame(self, height=120)
        footer.pack(fill="x", padx=20, pady=10)
        row1 = ctk.CTkFrame(footer, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=15)
        self.path_entry = ctk.CTkEntry(row1, textvariable=self.download_path, width=450, font=NORMAL_FONT)
        self.path_entry.pack(side="left", padx=10)
        ctk.CTkButton(row1, text="更改目录", font=NORMAL_FONT, command=self.browse).pack(side="left", padx=5)
        ctk.CTkButton(row1, text="打开目录", font=NORMAL_FONT, fg_color="transparent", border_width=1, text_color=("black", "white"), command=self.open_downloads).pack(side="left", padx=5)
        self.res_combo = ctk.CTkComboBox(row1, variable=self.res_var, values=["2160", "1440", "1080", "720"], font=NORMAL_FONT)
        self.res_combo.pack(side="right", padx=20)
        row2 = ctk.CTkFrame(footer, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=(0, 10))
        self.status_lbl = ctk.CTkLabel(row2, text="READY", font=SMALL_FONT, text_color="gray")
        self.status_lbl.pack(side="left", padx=10)
        self.p_bar = ctk.CTkProgressBar(row2, width=400)
        self.p_bar.pack(side="left", padx=20); self.p_bar.set(0)
        mode_box = ctk.CTkFrame(row2, fg_color="transparent")
        mode_box.pack(side="right", padx=20)
        ctk.CTkLabel(mode_box, text="外观:", font=SMALL_FONT).pack(side="left", padx=10)
        self.mode_map = {"浅色": "Light", "系统": "System", "深色": "Dark"}
        self.theme_segment = ctk.CTkSegmentedButton(mode_box, values=["浅色", "系统", "深色"], command=lambda m: ctk.set_appearance_mode(self.mode_map[m]), font=SMALL_FONT, width=180)
        self.theme_segment.set("系统")
        self.theme_segment.pack(side="left")

    def open_downloads(self):
        p = os.path.abspath(self.download_path.get())
        if not os.path.exists(p): os.makedirs(p)
        if os.name == 'nt': subprocess.Popen(['explorer', p])
        else: subprocess.Popen(['open', p])

    def dl_selection(self, key):
        selected = [cb for cb in self.scroll_items[key]["checkboxes"] if cb.get()]
        if not selected: return
        self.tabs.set("下载管理")
        threading.Thread(target=self.run_concurrent, args=(selected,), daemon=True).start()

    def run_concurrent(self, cbs):
        with ThreadPoolExecutor(max_workers=5) as exec:
            exec.map(self.dl_single, cbs)

    def dl_single(self, cb):
        if cb.url not in self.task_widgets:
            t_ui = TaskUI(self.task_scroll, title=cb.cget("text"), url=cb.url, fg_color=("gray90", "gray16"), corner_radius=10)
            t_ui.pack(fill="x", padx=10, pady=5)
            self.task_widgets[cb.url] = t_ui
        else: t_ui = self.task_widgets[cb.url]
        t_ui.status_label.configure(text="解析中...", text_color=THEME_BLUE)
        self.after(0, lambda: cb.configure(text_color=THEME_BLUE))
        def hook(d):
            if d['status'] == 'downloading':
                p = d.get('_percent_str', '0%').replace('%','')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                t_ui.p_bar.set(float(p)/100)
                t_ui.info_label.configure(text=f"速度: {speed} | 剩余: {eta}")
                t_ui.status_label.configure(text=f"{p}%")
        opts = {'format': f'bestvideo[height<={self.res_var.get()}]+bestaudio/best', 'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'), 'merge_output_format': 'mp4', 'ffmpeg_location': get_ffmpeg_path(), 'progress_hooks': [hook], 'quiet': True, 'noplaylist': True}
        try:
            with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([cb.url])
            t_ui.status_label.configure(text="完成", text_color=THEME_GREEN)
            t_ui.info_label.configure(text="")
            self.after(0, lambda: cb.configure(text_color=THEME_GREEN))
        except Exception as e:
            is_member = any(x in str(e) for x in ["members-only", "Join this channel", "Sign in if you've been granted access"])
            color = THEME_GOLD if is_member else THEME_RED
            status_text = "会员限制" if is_member else "下载失败"
            t_ui.status_label.configure(text=status_text, text_color=color)
            t_ui.info_label.configure(text="")
            self.after(0, lambda: cb.configure(text_color=color))

    def start_scan(self):
        u = self.url_input.get().strip()
        if not u: return
        targets = []
        if self.scan_videos.get(): targets.append(("videos", f"{u}/videos"))
        if self.scan_shorts.get(): targets.append(("shorts", f"{u}/shorts"))
        if self.scan_streams.get(): targets.append(("streams", f"{u}/streams"))
        for k in self.scroll_items:
            for w in self.scroll_items[k]["frame"].winfo_children(): w.destroy()
            self.scroll_items[k]["checkboxes"] = []
        for k, url in targets:
            self.scroll_items[k]["is_loading"] = True
            self.spin(k)
            threading.Thread(target=self.fetch, args=(k, url), daemon=True).start()

    def fetch(self, k, url):
        try:
            with yt_dlp.YoutubeDL({'extract_flat': True, 'quiet': True}) as ydl:
                entries = ydl.extract_info(url, download=False).get('entries', [])
                for e in entries:
                    if e:
                        cb = VideoCheckBox(self.scroll_items[k]["frame"], e.get('title','未知'), e.get('url'))
                        cb.pack(fill="x", padx=10, pady=3); cb.select()
                        if e.get('availability') == 'subscriber_only': cb.configure(text_color=THEME_GOLD)
                        self.scroll_items[k]["checkboxes"].append(cb)
        except: pass
        finally: self.scroll_items[k]["is_loading"] = False

    def spin(self, k, idx=0):
        if self.scroll_items[k]["is_loading"]:
            self.scroll_items[k]["icon_label"].configure(text=self.spinner_chars[idx%10], text_color=THEME_BLUE)
            self.after(100, lambda: self.spin(k, idx+1))
        else: self.scroll_items[k]["icon_label"].configure(text="OK", text_color=THEME_GREEN, font=("Arial", 10, "bold"))

    def toggle_inverse(self, k):
        for cb in self.scroll_items[k]["checkboxes"]:
            cb.deselect() if cb.get() else cb.select()

    def clear_tasks(self):
        for u, w in list(self.task_widgets.items()):
            if any(x in w.status_label.cget("text") for x in ["完成", "失败", "限制"]):
                w.destroy(); del self.task_widgets[u]

    def browse(self):
        p = filedialog.askdirectory()
        if p: self.download_path.set(os.path.abspath(p))

if __name__ == "__main__":
    app = ModernYoutubeApp()
    app.mainloop()