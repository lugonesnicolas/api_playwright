from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from playwright.async_api import async_playwright
import base64
import asyncio

app = FastAPI()

# Configuración del semáforo
MAX_CONCURRENT_REQUESTS = 4
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

class CaptureRequest(BaseModel):
    url: str

@app.post("/capture")
async def capture(request: CaptureRequest):
    async with semaphore:  # Limitar el número de conexiones concurrentes
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Navegar a la URL
                await page.goto(request.url)

                # Capturar la pantalla y convertirla a Base64
                screenshot_bytes = await page.screenshot(full_page=False)
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

                # Obtener el contenido HTML
                html_content = await page.content()

                await browser.close()

            # Devolver los datos al cliente
            return JSONResponse({
                "url": request.url,
                "screenshot_base64": screenshot_base64,
                "html_content": html_content
            })
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {str(e)}")

# Nuevo endpoint para solicitudes GET
@app.get("/test")
async def test(url: str = Query(..., description="URL de la página para capturar")):
    """
    Endpoint que permite capturar una página y devolver la captura y el HTML mediante una solicitud GET.
    """
    async with semaphore:  # Limitar el número de conexiones concurrentes
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Navegar a la URL
                await page.goto(url)

                # Capturar la pantalla completa
                screenshot_bytes = await page.screenshot(full_page=True)
                screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

                # Obtener el contenido HTML
                html_content = await page.content()

                await browser.close()

            # Crear el HTML que incluye la imagen como Base64
            html_response = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Captura de {url}</title>
            </head>
            <body>
                <h1>Captura de {url}</h1>
                <h2>Imagen Capturada:</h2>
                <img src="data:image/png;base64,{screenshot_base64}" alt="Captura de {url}" style="max-width: 100%; border: 1px solid #ddd;">
            </body>
            </html>
            """

            # Devolver el HTML
            return HTMLResponse(content=html_response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando la solicitud: {str(e)}")
