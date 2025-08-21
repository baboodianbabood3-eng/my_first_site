from flask import Flask, render_template , request, redirect, url_for
from urllib.parse import quote
from urllib.parse import unquote
import yt_dlp
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
        # use your Render secret file
        cookies_path = "/etc/secrets/cookies.txt"

        ydl_opts = {
            "cookiefile": cookies_path,
            "quiet": True,
            "skip_download": True,  # only fetch info, not video
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = info.get("formats", [])

        # Separate progressive & adaptive like you did with pytube
        progressive_streams = [
            f for f in formats if f.get("acodec") != "none" and f.get("vcodec") != "none"
        ]
        adaptive_streams = [
            f for f in formats if f.get("acodec") == "none" or f.get("vcodec") == "none"
        ]

        return render_template(
            "quality_version.html",
            title=info.get("title"),
            video_url=video_url,
            progressive_streams=progressive_streams,
            adaptive_streams=adaptive_streams,
        )

    except Exception as e:
        print("ERROR in quality_version:", e)
        return f"Error: {e}"


@app.route("/next_page")
def next_page():
    video_url = request.args.get("video_url")
    quality = request.args.get("quality")
    return f"Next page placeholder — URL: {video_url}, Quality: {quality}"

if __name__ == "__main__":
    app.run(debug=True)
