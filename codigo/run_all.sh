#!/bin/bash

echo "Comprobando entorno virtual..."
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Instalando dependencias necesarias..."
pip install --quiet numpy pandas openpyxl

echo "Limpiando resultados anteriores..."
rm -rf results_cec_batch
mkdir -p results_cec_batch

# Ejecutar los tres modos del benchmark uno a uno
declare -A MODOS
MODOS=( ["--std"]="HHO" ["--bl"]="HHO + Búsqueda Local" ["--blplus"]="HHO + BL Plus" )

for MODE in --std --bl --blplus
do
    echo "Ejecutando benchmark para ${MODOS[$MODE]}..."
    python3 src/batch_runner.py $MODE
done

echo "Generando Excel TacoLab combinado con todos los algoritmos..."
python3 src/generate_excel.py

echo ""
echo "¡Proceso completado con éxito!"
echo "Archivo generado: results_cec_batch/cec2017_ALL_algorithms.xlsx"
