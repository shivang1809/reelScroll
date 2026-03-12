import json
import yt_dlp

def app(environ, start_response):

    path = environ.get("PATH_INFO", "/")

    if path == "/":

        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <title>Reel Viewer</title>
        <style>
        body{
        margin:0;
        background:black;
        display:flex;
        align-items:center;
        justify-content:center;
        height:100vh;
        }
        video{
        height:90vh;
        border-radius:12px;
        }
        </style>
        </head>

        <body>

        <video id="reel" controls autoplay loop></video>

        <script>

        async function load(){

        const r = await fetch("/api");
        const data = await r.json();

        if(data.video){
            document.getElementById("reel").src = data.video;
        }else{
            document.body.innerHTML =
            "<pre style='color:white'>" +
            JSON.stringify(data,null,2) +
            "</pre>";
        }

        }

        load();

        </script>

        </body>
        </html>
        """

        start_response("200 OK",[("Content-Type","text/html")])
        return [html.encode()]


    if path == "/api":

        url = "https://www.instagram.com/reel/DAdV6R1BUib/"

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "best",
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept-Language": "en-US,en;q=0.9"
            }
        }

        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                video = info.get("url")

            response = {"video": video}

        except Exception as e:

            response = {"error": str(e)}

        start_response("200 OK",[("Content-Type","application/json")])
        return [json.dumps(response).encode()]


    start_response("404 Not Found",[("Content-Type","text/plain")])
    return [b"Not Found"]
