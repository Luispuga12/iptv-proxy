import os
from flask import Flask, redirect
import yt_dlp

app = Flask(__name__)

TARGET_URL = "https://www.dailymotion.com/video/x88epch"

@app.route('/')
def home():
    return "Proxy IPTV Anti-Bloqueo Activo"

@app.route('/canal.m3u8')
@app.route('/heraldo.m3u8')
def proxy_canal():
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            # Forzamos la suplantación de navegador para burlar a Cloudflare en la nube
            'extractor_args': {
                'generic': {
                    'impersonate': 'chrome'
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(TARGET_URL, download=False)
            stream_url = info.get('url')
            
            if stream_url:
                return redirect(stream_url, code=302)
                
        return "No se pudo extraer el enlace en vivo", 500
    except Exception as e:
        return f"Error al actualizar token: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
