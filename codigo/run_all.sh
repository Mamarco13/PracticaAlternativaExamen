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

echo "Ejecutando benchmark con batch_runner.py..."
python3 src/batch_runner.py

echo "Generando Excel final con generate_excel.py..."
python3 src/generate_excel.py

echo "¡Todo completado! Revisa results_cec_batch/cec2017_HHO_D30.xlsx"
