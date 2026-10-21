import os
from flask import Flask, redirect, abort
import requests
import yt_dlp
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

CANALES = {
    "heraldo": "https://www.dailymotion.com/video/x88epch",
    # Canal de tvplusgratis
    "golden_edge": "https://www.tvplusgratis.org/golden-edge-en-vivo.php"
}

@app.route('/')
def home():
    return "Proxy IPTV Activo"

def obtener_enlace_real(url_pagina):
    # Si es Dailymotion u otra plataforma directa, la dejamos pasar
    if "dailymotion.com" in url_pagina:
        return url_pagina
        
    # Si es de tvplusgratis, buscamos enlaces .m3u8 o fuentes ocultas en el código fuente
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        respuesta = requests.get(url_pagina, headers=headers, timeout=5)
        
        if respuesta.status_code == 200:
            # Buscamos con expresiones regulares cualquier URL .m3u8 oculta en el script
            match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', respuesta.text)
            if match:
                return match.group(1)
                
            # Como alternativa secundaria, buscamos iframes
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            iframe = soup.find('iframe')
            if iframe and iframe.get('src'):
                src = iframe.get('src')
                if src.startswith('//'):
                    src = 'https:' + src
                return src
    except Exception as e:
        print(f"Error al raspar la página: {e}")
        
    return url_pagina

@app.route('/<nombre_canal>.m3u8')
def proxy_canal(nombre_canal):
    if nombre_canal not in CANALES:
        abort(404, description="Canal no encontrado")
        
    url_base = CANALES[nombre_canal]
    
    # Obtenemos la URL real (si es tvplusgratis, extraerá el flujo o iframe interno)
    target_url = obtener_enlace_real(url_base)
    
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
