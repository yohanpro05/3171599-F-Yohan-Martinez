# ============================================
# DOCKERFILE - Proyecto API de Saludo
# ============================================

FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias con pip (más simple y confiable)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

EXPOSE 8000

# Comando correcto
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]