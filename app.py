from flask import Flask, render_template_string
import yt_dlp

app = Flask(__name__)

REEL_URL = "https://www.instagram.com/reel/DAdV6R1BUib/"

def get_video_url(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info.get("url")

@app.route("/")
def home():

    video = get_video_url(REEL_URL)

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <title>Reel Viewer</title>
    <style>
    body {{
        margin:0;
        background:black;
        display:flex;
        align-items:center;
        justify-content:center;
        height:100vh;
    }}

    video {{
        height:90vh;
        border-radius:12px;
    }}
    </style>
    </head>

    <body>
        <video src="{video}" autoplay controls loop></video>
    </body>
    </html>
    """

    return render_template_string(html)

if __name__ == "__main__":
    app.run(port=5000)
