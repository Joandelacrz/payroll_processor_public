# Usa Python 3.9 como base
FROM python:3.9

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 3000
EXPOSE 3000

# Comando de ejecución
CMD ["python", "main.py"]
