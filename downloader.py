import yt_dlp
import os
import shutil
import tempfile

def get_video_formats(video_url):
    try:
        secret_cookies_path = '/etc/secrets/cookies.txt'
        temp_cookies_path = os.path.join(tempfile.gettempdir(), 'cookies.txt')

        print(f"DEBUG: Copying cookies from {secret_cookies_path} to {temp_cookies_path}")
        shutil.copy(secret_cookies_path, temp_cookies_path)
        print("DEBUG: Copy successful")

        ydl_opts = {
            'cookiefile': temp_cookies_path,
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
                    'size': f"{(fmt.get('filesize') or fmt.get('filesize_approx') or 0) / (1024 * 1024):.2f} MB" if (fmt.get('filesize') or fmt.get('filesize_approx')) else "N/A"
                })

            return format_list, info.get('title')

    except Exception as e:
        print(f"ERROR: {e}")
        return [], f"Error: {e}"
