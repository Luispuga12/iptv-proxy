import os
import re
from flask import Flask, redirect, abort
import requests
from bs4 import BeautifulSoup
import yt_dlp

app = Flask(__name__)

CANALES = {
    "heraldo": "https://www.dailymotion.com/video/x88epch",
    "golden_edge": "https://www.tvplusgratis.org/golden-edge-en-vivo.php"
}

@app.route('/')
def home():
    return "Proxy IPTV Activo"

@app.route('/<nombre_canal>.m3u8')
def proxy_canal(nombre_canal):
    if nombre_canal not in CANALES:
        abort(404, description="Canal no encontrado")
        
    target_url = CANALES[nombre_canal]
    
    if "dailymotion.com" in target_url:
        ydl_opts = {'format': 'best', 'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            return redirect(info.get('url'), code=302)
            
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # 1. Entramos a la página principal del canal
        respuesta = requests.get(target_url, headers=headers, timeout=5)
        
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            # 2. Buscamos el iframe 'playerFrame' que descubrimos en la inspección
            iframe = soup.find('iframe', {'id': 'playerFrame'}) or soup.find('iframe')
            if iframe and iframe.get('src'):
                iframe_src = iframe.get('src')
                if iframe_src.startswith('//'):
                    iframe_src = 'https:' + iframe_src
                elif iframe_src.startswith('/'):
                    iframe_src = 'https://www.tvplusgratis.org' + iframe_src
                
                # 3. Entramos al contenido del core.php del iframe
                iframe_resp = requests.get(iframe_src, headers=headers, timeout=5)
                if iframe_resp.status_code == 200:
                    # 4. Buscamos el enlace .m3u8 final dentro del core.php
                    match = re.search(r'(https?://[^\s\'"]+\.m3u8[^\s\'"]*)', iframe_resp.text)
                    if match:
                        return redirect(match.group(1), code=302)
                        
        return "No se pudo extraer el flujo de video automáticamente", 500
    except Exception as e:
        return f"Error interno: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
