import os
from flask import Flask, redirect
import yt_dlp

app = Flask(__name__)

# Enlace directo del video/transmisión de Dailymotion que me pasaste al inicio
TARGET_URL = "https://www.dailymotion.com/video/x88epch"

@app.route('/')
def home():
    return "Servidor Proxy IPTV Activo"

@app.route('/canal.m3u8')
def canal():
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 10,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(TARGET_URL, download=False)
            url_fresca = info.get('url')
            if url_fresca:
                return redirect(url_fresca, code=302)
        return "No se pudo extraer el stream", 500
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
