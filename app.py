import os
from flask import Flask, redirect
import requests
from bs4aitan import BeautifulSoup
import re

app = Flask(__name__)

TARGET_URL = "https://heraldodemexico.com.mx/"

@app.route('/')
def home():
    return "Proxy IPTV Automático Activo"

@app.route('/heraldo.m3u8')
def canal():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://heraldodemexico.com.mx/"
    }
    try:
        # 1. Entramos a la página web del Heraldo para buscar el reproductor actual
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        
        # 2. Buscamos dentro del código HTML el enlace .m3u8 o el embed de Dailymotion vigente
        # Buscamos coincidencias de enlaces m3u8 o de video activos en el sitio
        match = re.search(r'https?://[^\s<>"]+?\.m3u8[^\s<>"]*', response.text)
        
        if match:
            url_fresca = match.group(0)
            # Redirigimos al reproductor hacia el enlace fresco recién encontrado
            return redirect(url_fresca, code=302)
        else:
            return "No se pudo encontrar un enlace m3u8 activo en este momento", 500

    except Exception as e:
        return f"Error al actualizar el token: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
