from flask import Flask, redirect
import yt_dlp

app = Flask(__name__)

# Usamos el enlace directo del video de Dailymotion para asegurar la extracción del stream
TARGET_URL = "https://www.dailymotion.com/video/x88epch"

@app.route('/')
def home():
    return "Proxy Local IPTV Activo y Automático"

@app.route('/canal.m3u8')
@app.route('/heraldo.m3u8')
def proxy_canal():
    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(TARGET_URL, download=False)
            stream_url = info.get('url')
            
            if stream_url:
                return redirect(stream_url, code=302)
                
        return "No se pudo extraer el enlace en vivo", 500
    except Exception as e:
        # Esto te mostrará el error exacto en la consola si algo falla
        print(f"Error detallado: {str(e)}")
        return f"Error al actualizar token: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
