#!/bin/bash

echo "Comprobando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Instalando dependencias..."
pip install --quiet numpy pandas openpyxl

# Leer modo desde argumento
# Leer modo desde argumento
FLAG="$1"

case "$FLAG" in
    --bl)
        echo "Modo Búsqueda Local activado (--bl)"
        rm -rf HHOBL
        ;;
    --blplus)
        echo "Modo Búsqueda Local Optimizada activado (--blplus)"
        rm -rf HHOBLplus
        ;;
    *)
        echo "Modo estándar HHO"
        rm -rf HHO
        FLAG=""
        ;;
esac

echo "Ejecutando benchmark con batch_runner.py..."
python3 src/batch_runner.py $FLAG

echo "Generando Excel final con generate_excel.py..."
python3 src/generate_excel.py $FLAG

echo "¡Todo completado! Revisa results_cec_batch/"
