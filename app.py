from flask import Flask, render_template , request, redirect, url_for
from downloader import get_video_formats  # ⬅️ Add this at the top of app.py
from urllib.parse import quote
from urllib.parse import unquote

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
        return redirect(url_for("quality_version", video_url=quote(video_url)))
    return render_template("takes_link.html")



@app.route("/quality_version")
def quality_version():
    video_url = request.args.get("video_url")
    video_url = unquote(video_url)  # decode back
    print("DEBUG quality_version video_url:", video_url)  # 👀 should be full URL
    formats, title = get_video_formats(video_url)
    return render_template("quality_version.html", video_url=video_url, formats=formats, title=title)


@app.route("/next_page")
def next_page():
    video_url = request.args.get("video_url")
    quality = request.args.get("quality")
    return f"Next page placeholder — URL: {video_url}, Quality: {quality}"

if __name__ == "__main__":
    app.run(debug=True)
