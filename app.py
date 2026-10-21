import os
from flask import Flask, redirect, abort
import yt_dlp

app = Flask(__name__)

# Diccionario con los canales y sus páginas de origen
CANALES = {
    "canal5": "https://www.tvplusgratis.org/canal-5-en-vivo.php",
    "heraldo": "https://www.dailymotion.com/video/x88epch"
}

@app.route('/')
def home():
    return "Proxy IPTV Activo"

@app.route('/<nombre_canal>.m3u8')
def proxy_canal(nombre_canal):
    if nombre_canal not in CANALES:
        abort(404, description="Canal no encontrado")
        
    target_url = CANALES[nombre_canal]
    
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            stream_url = info.get('url')
            
            if stream_url:
                return redirect(stream_url, code=302)
                
        return "No se pudo extraer el enlace en vivo", 500
    except Exception as e:
        return f"Error al actualizar token: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
