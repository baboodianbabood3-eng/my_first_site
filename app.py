from flask import Flask, render_template , request, redirect, url_for
from urllib.parse import quote
from urllib.parse import unquote
import yt_dlp
from downloader import download_video
from quality_version import get_video_formats
import os
from audio_downloader import download_audio
app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads/"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dub")
def dub():
    return render_template("dubber.html")

@app.route("/youtube")
def youtube():
    return render_template("language1.html")

@app.route("/language/<lang>")
def language(lang):
    return render_template("takes_link.html", lang=lang)

@app.route("/takes_link", methods=["GET", "POST"])
def takes_link():
    if request.method == "POST":
        video_url = request.form.get("video_url")

        # Normalize youtu.be URLs and remove extra query parameters
        if "youtu.be/" in video_url:
            video_url = video_url.replace("youtu.be/", "youtube.com/watch?v=")

        # Normalize Shorts URLs
        if "youtube.com/shorts/" in video_url:
            video_url = video_url.replace("/shorts/", "/watch?v=")

        print("DEBUG normalized video_url:", video_url)
        print("DEBUG takes_link video_url:", video_url)  # 👀 see actual input
        # Encode URL safely before redirect
        return redirect(f"/quality_version?video_url={video_url}")
    return render_template("takes_link.html")
@app.route("/quality_version")
def quality_version():
    video_url = request.args.get("video_url")
    if not video_url:
        return "Error: No video URL provided."

    try:
        # Normalize youtu.be links
        if "youtu.be/" in video_url:
            video_url = video_url.replace("youtu.be/", "youtube.com/watch?v=").split("?")[0]

        # Fetch formats using V2RayN proxy
        result = get_video_formats(video_url)  # no cookies

        # Optional: print qualities in console
        print(f"Available formats for {result['title']}:")
        for f in result["progressive"]:
            print(f"{f['format_id']}: {f['ext']} {f.get('resolution')} {f.get('fps', '')}fps")
        for f in result["adaptive"]:
            print(f"{f['format_id']}: {f['ext']} vcodec:{f.get('vcodec')} acodec:{f.get('acodec')}")

        return render_template(
            "quality_version.html",
            title=result["title"],
            video_url=video_url,
            progressive_streams=result["progressive"],
            adaptive_streams=result["adaptive"],
        )

    except Exception as e:
        print("ERROR in quality_version:", e)
        return f"Error: {e}"


@app.route("/download_and_process")
def download_and_process():
    video_url = request.args.get("video_url")
    format_id = request.args.get("quality")

    if not video_url or not format_id:
        return "Error: Missing video URL or quality"

    result = download_video(video_url, format_id, DOWNLOAD_FOLDER)

    if result["success"]:
        return f"Video downloaded successfully: {result['title']}"
    else:
        return f"Error downloading video: {result['error']}"


@app.route("/download_separate")
def download_separate():
    video_url = request.args.get("video_url")
    format_id = request.args.get("quality")

    if not video_url or not format_id:
        return "Error: Missing video URL or quality"

    # Download video
    video_result = download_video(video_url, format_id, DOWNLOAD_FOLDER)

    # Download audio
    audio_result = download_audio(video_url, DOWNLOAD_FOLDER)

    if video_result["success"] and audio_result["success"]:
        return f"Both downloaded successfully: {video_result['title']}"
    else:
        return f"Download failed - Video: {video_result.get('error', 'OK')}, Audio: {audio_result.get('error', 'OK')}"
@app.route("/next_page")
def next_page():
    video_url = request.args.get("video_url")
    quality = request.args.get("quality")
    return f"Next page placeholder — URL: {video_url}, Quality: {quality}"

if __name__ == "__main__":
    app.run(debug=True)
