import os
from flask import Flask, redirect, abort
import yt_dlp

app = Flask(__name__)

# Usamos directamente el enlace de embed que descubriste en la segunda imagen
CANALES = {
    "heraldo": "https://www.dailymotion.com/video/x88epch",
    "golden_edge": "https://embed.saohgdassregions.com/embed2/goldenedge.php"  # O el enlace de embed que te da la página
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
        
        # yt-dlp procesará directamente la página de embed sin necesidad de raspar HTML
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
