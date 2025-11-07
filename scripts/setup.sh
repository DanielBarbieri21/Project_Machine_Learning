#!/bin/bash
# Script de setup do projeto

echo "Configurando ambiente do projeto ML & Big Data..."

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/lake/raw
mkdir -p data/lake/processed
mkdir -p models
mkdir -p logs
mkdir -p orchestration/logs
mkdir -p orchestration/plugins

# Copiar arquivo de ambiente
if [ ! -f .env ]; then
    cp env.example .env
    echo "Arquivo .env criado. Por favor, configure as variáveis de ambiente."
fi

echo "Setup concluído!"

