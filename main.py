from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Downloader API V2 is running"

@app.route('/mp3')
def mp3():
    url = request.args.get('url')
    if not url:
        return 'Missing URL', 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'download.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f'Error: {str(e)}', 500

@app.route('/video')
def video():
    url = request.args.get('url')
    if not url:
        return 'Missing URL', 400

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'download.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename = filename.rsplit('.', 1)[0] + '.mp4'

        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
