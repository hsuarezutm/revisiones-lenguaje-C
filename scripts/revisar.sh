#!/bin/bash
mkdir -p resultados

for archivo in programas/*.c; do
    nombre=$(basename "$archivo" .c)
    salida="resultados/${nombre}.txt"
    echo "🔍 Revisando $archivo..." > "$salida"

    salida_compilacion=$(gcc -Wall -Wextra "$archivo" -o /dev/null 2>&1)
    estado=$?

    if [ $estado -eq 0 ]; then
        if echo "$salida_compilacion" | grep -qi "warning"; then
            echo "⚠️ Advertencias de compilación" >> "$salida"
            echo "$salida_compilacion" >> "$salida"
        else
            echo "✅ Compilación exitosa" >> "$salida"
        fi
    else
        echo "❌ Error de compilación" >> "$salida"
        echo "$salida_compilacion" >> "$salida"
    fi
done
