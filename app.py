import os
from flask import Flask, redirect, abort
from playwright.sync_api import sync_playwright

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

    try:
        enlace_m3u8 = None
        with sync_playwright() as p:
            # Lanzamos navegador con argumentos optimizados para Render (Docker)
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--single-process"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            def handle_request(route):
                nonlocal enlace_m3u8
                url = route.request.url
                # Filtramos para atrapar el .m3u8 real evitando peticiones de publicidad (vmap/ads)
                if ".m3u8" in url and "vmap" not in url and "ads" not in url and not enlace_m3u8:
                    enlace_m3u8 = url
                route.continue_()

            page.route("**/*", handle_request)
            
            # Cargamos la página del canal con un timeout controlado
            try:
                page.goto(target_url, timeout=15000, wait_until="domcontentloaded")
            except Exception:
                pass
            
            # Simulamos un clic para activar el reproductor si requiere interacción
            try:
                page.mouse.click(400, 300)
            except Exception:
                pass

            # Damos unos segundos extra para que pasen los anuncios y salte la lista del video real
            for _ in range(10):
                if enlace_m3u8:
                    break
                page.wait_for_timeout(1000)

            browser.close()

        if enlace_m3u8:
            return redirect(enlace_m3u8, code=302)
        else:
            return "No se pudo interceptar el enlace m3u8 del video", 500

    except Exception as e:
        return f"Error en automatización: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
