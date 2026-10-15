import os
from flask import Flask, redirect
import yt_dlp

app = Flask(__name__)

# URL de la página web de origen donde se aloja la transmisión en vivo
TARGET_URL = "https://heraldodemexico.com.mx/"

@app.route('/')
def home():
    return "Servidor Proxy IPTV Estable y Automático Activo"

@app.route('/heraldo.m3u8')
def generar_enlace_estable():
    try:
        # Configuración de yt-dlp para extraer únicamente el stream de video activo
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(TARGET_URL, download=False)
            
            # Extraemos la URL fresca con el token recién generado por el servidor de origen
            stream_url = info.get('url')
            
            if stream_url:
                # Redirigimos al reproductor IPTV hacia el enlace con el token actualizado al 100%
                return redirect(stream_url, code=302)
                
        return "No se pudo actualizar el token del stream", 500
    except Exception as e:
        return f"Error en el servidor proxy: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
