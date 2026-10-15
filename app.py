import os
from flask import Flask, redirect, abort
import yt_dlp

app = Flask(__name__)

# Diccionario central para todos tus canales sin importar de qué página sean
CANALES = {
    "heraldo": "https://www.dailymotion.com/ElHeraldoDeMexico",
    "canal5": "https://www.tvplusgratis.org/canal-5-en-vivo.php"

}

@app.route('/')
def home():
    return "Proxy IPTV Multicanal Activo"

@app.route('/stream/<nombre_canal>.m3u8')
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
            'extractor_args': {
                'generic': {
                    'impersonate': 'chrome'
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # yt-dlp analiza automáticamente la URL específica de ese canal, sin importar la página
            info = ydl.extract_info(target_url, download=False)
            stream_url = info.get('url')
            
            if stream_url:
                return redirect(stream_url, code=302)
                
        return "No se pudo extraer el enlace en vivo", 500
    except Exception as e:
        return f"Error al actualizar token: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
