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

            # Filter progressive streams (video + audio combined)
            progressive = [f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"]

            # Filter for important progressive qualities only
            important_progressive = []
            seen_resolutions = set()

            for f in progressive:
                height = f.get('height')

                # Only keep important resolutions and avoid duplicates
                if height:
                    if height <= 240 and '240' not in seen_resolutions:
                        important_progressive.append(f)
                        seen_resolutions.add('240')
                    elif height == 360 and '360' not in seen_resolutions:
                        important_progressive.append(f)
                        seen_resolutions.add('360')
                    elif height == 480 and '480' not in seen_resolutions:
                        important_progressive.append(f)
                        seen_resolutions.add('480')
                    elif height == 720 and '720' not in seen_resolutions:
                        important_progressive.append(f)
                        seen_resolutions.add('720')
                    elif height >= 1080 and '1080+' not in seen_resolutions:
                        important_progressive.append(f)
                        seen_resolutions.add('1080+')

            # Sort by quality (height)
            # Sort by quality (height)
            important_progressive.sort(key=lambda x: x.get('height', 0))

            # Add size information to each format
            for f in important_progressive:
                # Try to get file size from different sources
                size = f.get('filesize') or f.get('filesize_approx')
                if size:
                    f['size_mb'] = round(size / (1024 * 1024), 1)  # Convert to MB
                else:
                    # Estimate size based on bitrate and duration if available
                    tbr = f.get('tbr')  # total bitrate
                    duration = info.get('duration')
                    if tbr and duration:
                        estimated_size = (tbr * duration * 1000) / 8  # Convert to bytes
                        f['size_mb'] = round(estimated_size / (1024 * 1024), 1)
                    else:
                        f['size_mb'] = None

            return {
                "title": info.get("title", "Unknown"),
                "progressive": important_progressive,
                "adaptive": [],
            }
    except Exception as e:
        raise ValueError(f"Failed: {e}")
