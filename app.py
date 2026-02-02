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

    # Opções avançadas para evitar detecção de bot
    ydl_opts = {
        'format': 'best' if ext == 'mp4' else 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        # O segredo está aqui: simular um navegador comum
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Tenta extrair as informações sem baixar o arquivo no servidor
            info = ydl.extract_info(url, download=False)
            
            # Alguns vídeos do YT têm links que expiram ou exigem assinatura. 
            # Pegamos o link direto da mídia (URL do Google Video)
            return jsonify({
                "download_url": info['url'], 
                "title": info.get('title', 'video')
            })
    except Exception as e:
        error_msg = str(e)
        # Se ainda der erro de bot, mandamos uma mensagem mais clara
        if "Sign in to confirm" in error_msg:
            return jsonify({"error": "O YouTube bloqueou o servidor temporariamente por suspeita de bot. Tente novamente em alguns minutos ou com outro link."}), 403
        return jsonify({"error": error_msg}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
