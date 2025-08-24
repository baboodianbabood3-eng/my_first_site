from flask import Flask, render_template , request, redirect, url_for
from urllib.parse import quote
from urllib.parse import unquote
import yt_dlp
from quality_version import get_video_formats
import os
app = Flask(__name__)

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
@app.route("/quality_clean")
def quality_clean():
    video_url = request.args.get("video_url", "")
    if not video_url:
        return "Error: No video URL provided."

    try:
        # reuse your existing function
        result = get_video_formats(video_url)

        # define the wanted resolutions
        wanted_res = {"144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"}

        # filter progressive only
        progressive_clean = [
            f for f in result["progressive"]
            if f.get("resolution") in wanted_res
        ]

        # filter adaptive only
        adaptive_clean = [
            f for f in result["adaptive"]
            if f.get("resolution") in wanted_res
        ]

        return render_template(
            "quality_clean.html",
            title=result["title"],
            video_url=video_url,
            progressive_streams=progressive_clean,
            adaptive_streams=adaptive_clean,
        )

    except Exception as e:
        print("ERROR in quality_clean:", e)
        return f"Error: {e}"

@app.route("/next_page")
def next_page():
    video_url = request.args.get("video_url")
    quality = request.args.get("quality")
    return f"Next page placeholder — URL: {video_url}, Quality: {quality}"

if __name__ == "__main__":
    app.run(debug=True)
