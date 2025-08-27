import yt_dlp
import os

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}


def download_video(video_url: str, format_id: str, download_folder: str):
    """Download video with specified quality"""

    # Create download folder if it doesn't exist
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    ydl_opts = {
        "proxy": PROXIES["https"],
        "cookiesfrombrowser": ("firefox",),
        "format": f"{format_id}+bestaudio[ext=m4a]/best",  # Download specific quality
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "socket_timeout": 30,
        "retries": 2,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            return {
                "success": True,
                "filename": filename,
                "title": info.get("title", "Unknown"),
                "file_path": filename
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
