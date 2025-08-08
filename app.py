from flask import Flask, render_template , request, redirect, url_for
from downloader import get_video_formats  # ⬅️ Add this at the top of app.py

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
        return redirect(url_for("quality_version", video_url=video_url))
    return render_template("takes_link.html")

@app.route("/quality_version")
def quality_version():
    video_url = request.args.get("video_url")
    formats, title = get_video_formats(video_url)
    return render_template("quality_version.html", video_url=video_url, formats=formats, title=title)


if __name__ == "__main__":
    app.run(debug=True)
