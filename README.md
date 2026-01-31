# YouTube Downloader

YouTube Downloader是一款高性能、多线程的视频归档工具。它专为需要极速解析与批量下载的用户设计，采用 CustomTkinter 框架构建。

## 核心功能

* **精准分流扫描**：支持在开始扫描前预选分类（普通视频、短视频、直播回放），大幅减少解析冗余数据的时间。
* **多线程并行下载**：内置 5 线程并发下载引擎，充分利用高带宽网络环境进行任务狂飙。
* **超高清画质支持**：默认支持最高 2160p (4K) 视频流抓取，并自动调用二进制工具进行无损封装。
* **实时下载管理**：提供独立的任务监控页面，显示当前下载速度、进度百分比及预估剩余时间 (ETA)。
* **系统主题同步**：界面自动适配 Windows 系统颜色模式（深色/浅色），并支持手动自由切换。
* **会员状态识别**：智能检测会员限定视频，并在任务状态栏明确提示“会员限制”，避免因权限不足导致的无效挂机。
* **一键目录直达**：集成全局“打开目录”功能，下载完成后可快速定位本地物理路径。

## 技术栈

* **核心引擎**: yt-dlp
* **图形界面**: CustomTkinter
* **二进制组件**: FFmpeg
* **开发语言**: Python 3.10+

## 安装与运行

1. **配置环境**
   安装必要的 Python 依赖包：
   `pip install yt-dlp customtkinter`

2. **部署二进制文件**
   从官方源下载 [FFmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)，解压并将 `ffmpeg.exe` 放置在 `main.py` 的同级目录下。

3. **启动程序**
   执行 `python main.py` 启动软件。

## 封装发布

如需将项目打包为独立的 .exe 文件，请使用以下 PyInstaller 指令：

`pyinstaller --noconsole --onefile --add-binary "ffmpeg.exe;." --collect-all customtkinter --name "YouTube_Downloader_Rinne" main.py`

## 免责声明

本工具仅供个人学习、研究及视频归档使用。用户在使用过程中应严格遵守 YouTube 官方服务条款及所在地法律法规。作者不对任何违规使用行为承担法律责任。
