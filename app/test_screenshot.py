import time
import requests
import base64


# Registrar el tiempo de inicio
start_time = time.time()

# Configuración
url = "https://api-playwright.onrender.com/capture"  # Endpoint de tu API
data = {
    "url": "https://www.amazon.ae/Head-Shoulders-Daily-Anti-Dandruff-Shampoo/dp/B098CZJ5QZ/?_encoding=UTF8&pd_rd_w=eVIcT&content-id=amzn1.sym.b6b75a08-3730-42cf-a68a-48bde5cc4a0d%3Aamzn1.symc.9b8fba90-e74e-4690-b98f-edc36fe735a6&pf_rd_p=b6b75a08-3730-42cf-a68a-48bde5cc4a0d&pf_rd_r=ZP0144ZMS8ZAW8AVKPVE&pd_rd_wg=oPrm1&pd_rd_r=320e99fd-0273-44c1-9b80-f195cf4ff7b5&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d",  # URL para capturar
    "output_file": "example_screenshot.png"  # Nombre del archivo de salida
}

for i in range(0, 10):
    # Solicitud al endpoint
    response = requests.post(url, json=data)

    # Guardar la imagen si la respuesta es exitosa
    if response.status_code == 200:
        result = response.json()
        screenshot_data = base64.b64decode(result["screenshot_base64"])
        with open("images/example_screenshot.png", "wb") as f:
            f.write(screenshot_data)
        print("Captura de pantalla guardada como example_screenshot.png")
    else:
        print(f"Error: {response.status_code}, {response.text}")
        
# Registrar el tiempo de fin
end_time = time.time()

# Calcular el tiempo de ejecución
execution_time = end_time - start_time
print(f"Tiempo de ejecución: {execution_time:.6f} segundos")