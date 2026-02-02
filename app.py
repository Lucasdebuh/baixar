import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    ext = data.get('format')

    ydl_opts = {
        'format': 'best' if ext == 'mp4' else 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        # Importante para rodar no servidor:
        'nocheckcertificate': True,
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            # Pegamos o link direto da mídia
            return jsonify({"download_url": info['url'], "title": info.get('title', 'video')})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)