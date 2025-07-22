#!/bin/sh
set -e

echo "Esperando o banco subir…"
/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Banco pronto, iniciando Django…"

cd /app/backend

echo "Aplicando migrations…"
python manage.py migrate

echo "Subindo servidor Django…"
python manage.py runserver 0.0.0.0:8000
