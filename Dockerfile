# Usar la imagen oficial de Python
FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos y el archivo .env primero
COPY requirements.txt .env ./

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
# Asegúrate de que los nombres de archivos son correctos
COPY . .

# Comando para ejecutar el script principal
CMD ["python", "main.py"]

