#!/bin/bash

mkdir -p resultados

for archivo in programas/*.c; do
    nombre=$(basename "$archivo" .c)
    salida="resultados/${nombre}.txt"
    echo "🔍 Revisando $archivo..." > "$salida"

    # Compilación con gcc, capturando errores y advertencias
    salida_compilacion=$(gcc -Wall -Wextra "$archivo" -o /dev/null 2>&1)

    if [ $? -eq 0 ]; then
        echo "✅ Compilación exitosa" >> "$salida"
    else
        echo "❌ Error de compilación o advertencias" >> "$salida"
        echo "$salida_compilacion" >> "$salida"
    fi
done
