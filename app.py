import json
import yt_dlp

def app(environ, start_response):

    path = environ.get("PATH_INFO", "/")

    # homepage
    if path == "/":

        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8">
        <title>Instagram Reel Viewer</title>

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

        const res = await fetch('/api');
        const data = await res.json();

        if(data.video){
            document.getElementById("reel").src = data.video;
        }else{
            document.body.innerHTML="<h2 style='color:white'>Failed to load video</h2>";
        }

        }

        load();

        </script>

        </body>
        </html>
        """

        start_response("200 OK", [("Content-Type", "text/html")])
        return [html.encode()]

    # api route
    if path == "/api":

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

    start_response("404 Not Found", [("Content-Type","text/plain")])
    return [b"Not Found"]
