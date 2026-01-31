# YouTube Downloader

YouTube Downloader是一款高性能、多线程的视频归档工具。它专为需要极速解析与批量下载的用户设计，采用 CustomTkinter 框架构建，具备清爽的视觉界面。

YouTube Downloader is a high-performance, multi-threaded video archiving utility. Designed for power users who require rapid parsing and batch downloading, it is built on the CustomTkinter framework to provide a clean visual interface.

---

## 核心功能 | Key Features

* **精准分流扫描 (Precise Categorized Scanning)**: 
  支持在开始扫描前预选分类（普通视频、短视频、直播回放），大幅减少解析冗余数据的时间。
  Allows users to pre-select content types before scanning, significantly reducing the time spent parsing redundant data.

* **多线程并行下载 (5-Thread Parallel Downloads)**: 
  内置 5 线程并发下载引擎，充分利用高带宽网络环境进行任务狂飙。
  Equipped with a built-in 5-thread concurrent download engine to maximize bandwidth utilization.

* **超高清画质支持 (4K UHD Support)**: 
  默认支持最高 2160p (4K) 视频流抓取，并自动调用二进制工具进行无损封装。
  Natively supports capturing video streams up to 2160p (4K) and utilizes binary tools for lossless muxing.

* **实时下载管理 (Real-time Task Management)**: 
  提供独立的任务监控页面，显示当前下载速度、进度百分比及预估剩余时间 (ETA)。
  Features a dedicated task monitoring page displaying live download speeds, progress percentages, and ETA.

* **系统主题同步 (System Theme Synchronization)**: 
  界面自动适配 Windows 系统颜色模式（深色/浅色），并支持手动自由切换。
  The UI automatically adapts to Windows color schemes (Dark/Light) and supports manual toggle.

* **会员状态识别 (Membership Detection)**: 
  智能检测会员限定视频，并在任务状态栏明确提示“会员限制”，避免无效挂机。
  Identifies membership-restricted videos and provides a clear "Membership Restriction" status to prevent wasted idle time.

* **一键目录直达 (Instant Directory Access)**: 
  集成全局“打开目录”功能，下载完成后可快速定位本地物理路径。
  Integrated global "Open Directory" function for immediate access to the download path.

---

## 技术栈 | Technology Stack

* **Core Engine**: yt-dlp
* **GUI Framework**: CustomTkinter
* **Binary Tools**: FFmpeg
* **Language**: Python 3.10+

---

## 安装与运行 | Installation and Execution

1. **安装依赖 (Install Dependencies)**:
   使用提供的 `requirements.txt` 安装必要的 Python 组件：
   Install the required Python packages using the provided `requirements.txt`:
   `pip install -r requirements.txt`

2. **部署二进制文件 (Deploy Binary Tools)**:
   从官方源下载 [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)，解压并将 `ffmpeg.exe` 放置在 `main.py` 的同级目录下。
   Download FFmpeg, extract it, and place `ffmpeg.exe` in the same directory as `main.py`.

3. **启动程序 (Launch Program)**:
   执行 `python main.py` 启动软件。
   Run `python main.py` to start the application.

---

## 封装发布 | Packaging and Deployment

如需将项目打包为独立的 .exe 文件，请使用以下 PyInstaller 指令：
To compile the project into a standalone .exe file, use the following PyInstaller command:

`pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --collect-all customtkinter --name "YouTube_Downloader_Rinne" main.py`

---

## 免责声明 | Disclaimer

本工具仅供个人学习、研究及视频归档使用。用户应严格遵守 YouTube 官方服务条款及所在地法律法规。作者不对任何违规使用行为承担法律责任。
This tool is intended solely for personal study and research. Users must comply with YouTube's Terms of Service and local laws. The author assumes no liability for unauthorized use.
