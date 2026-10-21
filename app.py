import os
from flask import Flask, redirect, abort
from playwright.sync_api import sync_playwright
import yt_dlp

app = Flask(__name__)

CANALES = {
    "heraldo": "https://www.dailymotion.com/video/x88epch",
    "canal_5": "https://telelibre.st/en-vivo/canal-5/"
}

@app.route('/')
def home():
    return "Proxy IPTV con Automatización Activo"

@app.route('/<nombre_canal>.m3u8')
def proxy_canal(nombre_canal):
    if nombre_canal not in CANALES:
        abort(404, description="Canal no encontrado")
        
    target_url = CANALES[nombre_canal]
    
    # Si es Dailymotion, usa yt-dlp normalmente
    if "dailymotion.com" in target_url:
        try:
            ydl_opts = {'format': 'best', 'quiet': True, 'skip_download': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=False)
                return redirect(info.get('url'), code=302)
        except Exception as e:
            return f"Error yt-dlp: {str(e)}", 500

    # Si es Tele Libre, usamos Playwright para cazar el token m3u8 al vuelo en la red
    try:
        enlace_m3u8 = None
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
            page = browser.new_page()
            
            def handle_request(route):
                nonlocal enlace_m3u8
                url = route.request.url
                if ".m3u8" in url and not enlace_m3u8:
                    enlace_m3u8 = url
                route.continue_()
                
            page.route("**/*", handle_request)
            page.goto(target_url, timeout=30000)
            
            try:
                page.wait_for_timeout(5000) # Espera a que el reproductor dispare la petición
            except:
                pass
                
            browser.close()
            
        if enlace_m3u8:
            return redirect(enlace_m3u8, code=302)
        else:
            return "No se pudo interceptar el enlace m3u8 automáticamente", 500
            
    except Exception as e:
        return f"Error de automatización: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
