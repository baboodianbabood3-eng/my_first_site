import yt_dlp
import os

def get_video_formats(video_url):
    try:
        # Path to your cookies2.txt file
        cookie_file_path = os.path.abspath('cookies2.txt')

        ydl_opts = {
            'cookiefile': cookie_file_path,
            'verbose': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get('formats', [])

            format_list = []
            for fmt in formats:
                format_list.append({
                    'id': fmt.get('format_id'),
                    'ext': fmt.get('ext'),
                    'resolution': fmt.get('resolution') or f"{fmt.get('width')}x{fmt.get('height')}",
                    'fps': fmt.get('fps', ''),
                    'vcodec': fmt.get('vcodec'),
                    'acodec': fmt.get('acodec'),
                    'size': f"{(fmt.get('filesize') or fmt.get('filesize_approx') or 0) / (1024 * 1024):.2f} MB"
                            if (fmt.get('filesize') or fmt.get('filesize_approx')) else "N/A"
                })

            return format_list, info.get('title')

    except Exception as e:
        print(f"ERROR: {e}")
        return [], f"Error: {e}"
