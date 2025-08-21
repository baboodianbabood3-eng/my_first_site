import yt_dlp

def get_video_formats(video_url):
    try:
        ydl_opts = {
            "cookiefile": "/etc/secrets/cookies.txt"  # <-- use secret file path
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])
            return formats, info.get("title")

    except Exception as e:
        return [], f"Error: {e}"
