import json
import yt_dlp

def app(environ, start_response):

    url = "https://www.instagram.com/reel/DAdV6R1BUib/"

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "format": "best"
    }

    video = None

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video = info.get("url")
    except Exception as e:
        response = json.dumps({"error": str(e)})
        start_response("500 Internal Server Error", [("Content-Type","application/json")])
        return [response.encode()]

    response = json.dumps({"video": video})

    start_response("200 OK", [("Content-Type","application/json")])

    return [response.encode()]
