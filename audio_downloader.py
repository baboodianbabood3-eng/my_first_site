import yt_dlp
import os

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}


def download_audio(video_url: str, download_folder: str):
    """Download only the best audio"""

    ydl_opts = {
        "proxy": PROXIES["https"],
        "cookiesfrombrowser": ("firefox",),
        "format": "bestaudio[ext=m4a]",
        "outtmpl": os.path.join(download_folder, "%(title)s_audio.%(ext)s"),
        "socket_timeout": 30,
        "retries": 2,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                "success": True,
                "audio_file": filename,
                "title": info.get("title", "Unknown")
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }