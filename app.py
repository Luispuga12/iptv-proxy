import os
import re
from flask import Flask, redirect, abort
import requests
import yt_dlp

app = Flask(__name__)

CANALES = {
    "heraldo": "https://www.dailymotion.com/video/x88epch",
    "golden_edge": "https://embed.saohgdassregions.com/embed2/goldenedge.php"
}

@app.route('/')
def home():
    return "Proxy IPTV Activo"

@app.route('/<nombre_canal>.m3u8')
def proxy_canal(nombre_canal):
    if nombre_canal not in CANALES:
        abort(404, description="Canal no encontrado")
        
    target_url = CANALES[nombre_canal]
    
    # OPCIÓN A: Si es Dailymotion u otra plataforma soportada por yt-dlp
    if "dailymotion.com" in target_url or "youtube.com" in target_url:
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
        except Exception as e:
            return f"Error con yt-dlp: {str(e)}", 500

    # OPCIÓN B: Si es un reproductor web de saohgdassregions u otra fuente no soportada por yt-dlp
    else:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tvplusgratis.org/'
            }
            respuesta = requests.get(target_url, headers=headers, timeout=5)
            
            if respuesta.status_code == 200:
                # Busca directamente la URL que contiene el archivo .m3u8 dentro del código JavaScript/HTML
                match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', respuesta.text)
                if match:
                    stream_url = match.group(1)
                    return redirect(stream_url, code=302)
                    
            return "No se encontró enlace .m3u8 activo en la página", 500
        except Exception as e:
            return f"Error al extraer enlace directo: {str(e)}", 500

    return "No se pudo procesar el canal", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
