#!/bin/bash
# Script para executar testes

echo "Executando testes..."

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate  # Windows
fi

# Executar testes
pytest tests/ -v --cov=. --cov-report=html

echo "Testes concluídos!"

