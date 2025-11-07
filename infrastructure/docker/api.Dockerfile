FROM python:3.9-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY api/ /app/api/
COPY ml/ /app/ml/
COPY data_ingestion/ /app/data_ingestion/
COPY data_processing/ /app/data_processing/

# Expor porta
EXPOSE 8000

# Comando para executar a API
CMD ["python", "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]

