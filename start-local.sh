#!/bin/bash

echo "========================================================"
echo "               Iniciando Gymnatic Localhost"
echo "========================================================"
echo ""

# Obtener la ruta base del script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

echo "1. Iniciando servidor Backend (FastAPI) en http://localhost:8000..."

(
    cd "$DIR/backend" || exit 1
    source venv/bin/activate
    uvicorn app.main:app --host 0.0.0.0 --port 8000
) &

BACKEND_PID=$!

echo "2. Iniciando servidor Frontend (Next.js) en http://localhost:3000..."

(
    cd "$DIR/frontend" || exit 1
    npm run dev
) &

FRONTEND_PID=$!

echo ""
echo "========================================================"
echo "Servidores iniciados con éxito!"
echo "- Frontend: http://localhost:3000"
echo "- Backend API Docs: http://localhost:8000/docs"
echo "Presioná Ctrl+C para detener ambos servidores."
echo "========================================================"
echo ""

# Cerrar ambos servidores al presionar Ctrl+C
cleanup() {
    echo ""
    echo "Deteniendo servidores..."

    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null

    wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null

    echo "Servidores detenidos."
    exit 0
}

trap cleanup INT TERM

# Mantener el script ejecutándose
wait
