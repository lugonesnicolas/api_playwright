from fastapi import FastAPI
from pydantic import BaseModel
from playwright.async_api import async_playwright
from fastapi.responses import JSONResponse
import base64

app = FastAPI()

class CaptureRequest(BaseModel):
    url: str

@app.post("/capture")
async def capture(request: CaptureRequest):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navegar a la URL
        await page.goto(request.url)

        # Capturar la pantalla y convertirla a Base64
        screenshot_bytes = await page.screenshot(full_page=True)
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