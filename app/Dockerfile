FROM mcr.microsoft.com/playwright:v1.49.1-noble

# Instalar Python y pip si no están disponibles
RUN apt-get update && apt-get install -y python3 python3-pip

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias de Python
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto de FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
