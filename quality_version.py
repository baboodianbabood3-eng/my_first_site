from pytube import YouTube

def list_qualities(url):
    try:
        yt = YouTube(url)
        print(f"Title: {yt.title}\n")

        # Get all streams with video + audio (progressive)
        print("Available Progressive Streams (video + audio):")
        for stream in yt.streams.filter(progressive=True, file_extension="mp4"):
            print(f"itag: {stream.itag}, resolution: {stream.resolution}, fps: {stream.fps}, mime_type: {stream.mime_type}")

        print("\nAvailable Adaptive Streams (video only / audio only):")
        for stream in yt.streams.filter(progressive=False):
            print(f"itag: {stream.itag}, type: {stream.type}, resolution: {stream.resolution}, abr: {stream.abr}")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    url = input("Enter YouTube URL: ")
    list_qualities(url)
