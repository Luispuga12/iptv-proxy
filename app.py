import os
from flask import Flask, redirect
import requests

app = Flask(__name__)

# ID del video de Dailymotion que extrajiste de la URL original (x88epch)
VIDEO_ID = "x88epch"

@app.route('/')
def home():
    return "Proxy IPTV Dailymotion API Activo"

@app.route('/heraldo.m3u8')
def canal():
    try:
        # Consultamos la API oficial de Dailymotion para obtener los metadatos y enlaces del video
        api_url = f"https://www.dailymotion.com/player/metadata/video/{VIDEO_ID}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(api_url, headers=headers, timeout=10)
        data = response.json()
        
        # Buscamos dentro de la respuesta de la API el enlace de calidad HLS/m3u8 disponible
        qualities = data.get("qualities", {})
        stream_url = None
        
        # Intentamos buscar la mejor calidad disponible en el JSON de Dailymotion
        for q in ["auto", "1080", "720", "480", "360"]:
            if q in qualities and isinstance(qualities[q], list) and len(qualities[q]) > 0:
                for item in qualities[q]:
                    if "url" in item and item["url"].endswith(".m3u8"):
                        stream_url = item["url"]
                        break
            if stream_url:
                break
                
        # Si encontramos el enlace fresco, redirigimos automáticamente a Kodi
        if stream_url:
            return redirect(stream_url, code=302)
        else:
            return "No se pudo obtener el stream de la API", 500

    except Exception as e:
        return f"Error al procesar la API: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
