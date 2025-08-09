import yt_dlp

def get_video_formats(video_url):
    try:
        ydl_opts = {
            'cookiefile': '/etc/secrets/cookies.txt'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            format_list = []
            for fmt in formats:
                format_id = fmt.get('format_id')
                ext = fmt.get('ext')
                resolution = fmt.get('resolution') or f"{fmt.get('width')}x{fmt.get('height')}"
                fps = fmt.get('fps', '')
                vcodec = fmt.get('vcodec')
                acodec = fmt.get('acodec')
                filesize = fmt.get('filesize') or fmt.get('filesize_approx')
                size_mb = f"{filesize / (1024 * 1024):.2f} MB" if filesize else "N/A"

                format_list.append({
                    'id': format_id,
                    'ext': ext,
                    'resolution': resolution,
                    'fps': fps,
                    'vcodec': vcodec,
                    'acodec': acodec,
                    'size': size_mb
                })
            return format_list, info.get('title')
    except Exception as e:
        return [], f"Error: {e}"
