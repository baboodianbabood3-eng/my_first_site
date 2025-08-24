import yt_dlp

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}


def get_video_formats(video_url: str, cookies_path: str = None):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "proxy": PROXIES["https"],  # Add proxy back
        "noplaylist": True,
        "cookiesfrombrowser": ("firefox",),
        "socket_timeout": 30,  # Increase timeout
        "retries": 2,  # Reduce retries
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])

            progressive = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"]
            adaptive = [f for f in formats if f.get("acodec") == "none" or f.get("vcodec") == "none"]

            return {
                "title": info.get("title", "Unknown"),
                "progressive": progressive,
                "adaptive": adaptive,
            }
    except Exception as e:
        raise ValueError(f"Failed: {e}")
