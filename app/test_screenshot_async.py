import asyncio
import httpx
import json
import base64
import os

# Configuración
HTML_FOLDER = r"app\html"
SCREENSHOT_FOLDER = r"app\images"
BASE_URL = "http://localhost:8000/capture"
JSON_FILE = "dia.json"

# Función para cargar los datos del JSON
def load_links(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

# Función para enviar una solicitud y guardar los archivos
async def send_request(data):
    timeout = httpx.Timeout(30)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(BASE_URL, json={"url": data["url"]})
        if response.status_code == 200:
            result = response.json()

            # Guardar la captura de pantalla
            screenshot_data = base64.b64decode(result["screenshot_base64"])
            screenshot_path = os.path.join(SCREENSHOT_FOLDER, data["screenshot_file"])
            with open(screenshot_path + data["screenshot_file"], "wb") as screenshot_file:
                screenshot_file.write(screenshot_data)

            # Guardar el contenido HTML
            html_path = os.path.join(HTML_FOLDER, data["html_file"])
            with open(html_path + data["html_file"], "w", encoding="utf-8") as html_file:
                html_file.write(result["html_content"])

            print(f"Archivos guardados para {data['url']}")
        else:
            print(f"Error para {data['url']}: {response.status_code}, {response.text}")

# Función principal
async def main():
    links = load_links(JSON_FILE)
    tasks = [send_request(link) for link in links]
    await asyncio.gather(*tasks)
if __name__ == "__main__":
    asyncio.run(main())
