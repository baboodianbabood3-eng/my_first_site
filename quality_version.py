import yt_dlp

PROXIES = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}


def get_video_formats(video_url: str, cookies_path: str = None):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "proxy": PROXIES["https"],
        "noplaylist": True,
        "cookiesfrombrowser": ("firefox",),
        "socket_timeout": 30,
        "retries": 2,
        "extract_flat": False,  # Ensure full info extraction
        "listformats": True,  # This forces yt-dlp to get detailed format info
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
            # Add size information to each format
            # Debug: Check what size info yt-dlp provides
            for f in important_progressive:
                print(
                    f"Format {f.get('format_id')}: filesize={f.get('filesize')}, filesize_approx={f.get('filesize_approx')}")

            # Add size information to each format
            # Add size information to each format
            for f in important_progressive:
                # Try to get file size from different sources
                size = f.get('filesize') or f.get('filesize_approx')
                if size:
                    f['size_mb'] = round(size / (1024 * 1024), 1)  # Convert to MB
                else:
                    # More accurate estimation based on actual YouTube compression
                    height = f.get('height', 0)
                    duration = info.get('duration', 0)
                    fps = f.get('fps', 25)

                    if height and duration:
                        # More realistic bitrate calculation based on YouTube's actual compression
                        # These are based on typical YouTube progressive stream bitrates
                        if height <= 144:
                            base_bitrate = 95  # kbps
                        elif height <= 240:
                            base_bitrate = 130  # kbps
                        elif height <= 360:
                            base_bitrate = 230  # kbps
                        elif height <= 480:
                            base_bitrate = 375  # kbps
                        elif height <= 720:
                            base_bitrate = 750  # kbps
                        else:  # 1080p+
                            base_bitrate = 1350  # kbps

                        # Adjust for fps (higher fps = slightly higher bitrate)
                        fps_multiplier = min(fps / 25.0, 1.2)  # Max 20% increase
                        adjusted_bitrate = base_bitrate * fps_multiplier

                        # Calculate size with 10% buffer for overhead
                        estimated_size = (adjusted_bitrate * duration * 1.1) / 8 / 1024
                        f['size_mb'] = round(estimated_size, 1)
                    else:
                        f['size_mb'] = None

            return {
                "title": info.get("title", "Unknown"),
                "progressive": important_progressive,
                "adaptive": [],
            }
    except Exception as e:
        raise ValueError(f"Failed: {e}")
