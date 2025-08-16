# downloader.py
from pytube import YouTube

def get_video_formats(url):
    yt = YouTube(url)
    formats = []

    # Video+Audio streams
    for stream in yt.streams.filter(progressive=True, file_extension="mp4"):
        formats.append({
            "itag": stream.itag,
            "type": "video+audio",
            "resolution": stream.resolution,
            "mime_type": stream.mime_type,
        })

    # Video only streams
    for stream in yt.streams.filter(only_video=True, file_extension="mp4"):
        formats.append({
            "itag": stream.itag,
            "type": "video",
            "resolution": stream.resolution,
            "mime_type": stream.mime_type,
        })

    # Audio only streams
    for stream in yt.streams.filter(only_audio=True):
        formats.append({
            "itag": stream.itag,
            "type": "audio",
            "resolution": stream.abr,  # audio bitrate
            "mime_type": stream.mime_type,
        })

    return formats, yt.title
