# YouTube-Downloader

A high-performance, multi-threaded YouTube downloader with a modern CustomTkinter GUI. Features 4K support, categorized scanning, and system-sync theme.
Supports preset categorization before scanning (standard videos, short videos, live stream replays), significantly boosting parsing efficiency.
Built-in 5-thread concurrent downloads.
Default support for capturing and automatically merging video streams up to 2160p (4K).
Dedicated download management page for real-time monitoring of download speed, progress, and remaining time.
Theme Sync: UI seamlessly adapts to Windows color schemes, supporting light, dark, and system-following modes.
Automatically detects membership-restricted videos and displays clear “Membership Restriction” alerts to prevent wasted idle time.
If you need to package it yourself, please import ffmpeg.exe (https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z，Extract ffmpeg.exe after downloading) into the same directory as main.py.
Disclaimer：This tool is intended solely for personal study, research, and video archiving purposes. Please use it in compliance with YouTube's official Terms of Service and applicable local copyright laws.

一款高性能、多线程的YouTube下载器，配备现代化的CustomTkinter图形界面。支持4K视频下载、分类扫描功能及系统同步主题。
支持在扫描前预设分类（普通视频、短视频、直播回放），大幅提升解析效率。
内置 5 线程并发下载。
默认支持最高 2160p (4K) 视频流抓取与自动合并。
独立的下载管理页面，实时监控下载速度、进度及剩余时间。
UI 完美适配 Windows 系统颜色模式，支持浅色、深色及系统跟随。
自动检测会员限定视频并弹出明确的“会员限制”提醒，避免无效挂机。
如需自行打包，请在main.py同目录下导入ffmpeg.exe（https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z下载后解压提取ffmpeg.exe）
免责声明：本工具仅供个人学习研究及视频归档使用，请在遵守 YouTube 官方服务条款及当地版权法律的前提下使用。

Technology Stack
Core Engine: yt-dlp
GUI Framework: CustomTkinter
Binary Tools: FFmpeg (for muxing)
Language: Python 3.10+
