.PHONY: help setup install test lint format run clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup      - Configura o ambiente do projeto"
	@echo "  make install    - Instala as dependências"
	@echo "  make test       - Executa os testes"
	@echo "  make lint       - Executa o linter"
	@echo "  make format     - Formata o código"
	@echo "  make run        - Inicia os serviços"
	@echo "  make clean      - Limpa arquivos temporários"

setup:
	bash scripts/setup.sh

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	flake8 . --max-line-length=100 --exclude=venv,__pycache__,.git

format:
	black . --exclude=venv

run:
	docker-compose up -d

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

