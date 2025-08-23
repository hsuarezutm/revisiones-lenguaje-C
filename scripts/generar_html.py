import os
import shutil

html = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe de Programas en C</title>
  <style>
    body {
      font-family: sans-serif;
      padding: 2em;
      transition: background 0.3s, color 0.3s;
      background: var(--bg);
      color: var(--fg);
    }
    .tarjeta {
      background: var(--card-bg);
      border-radius: 8px;
      padding: 1em;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      margin-bottom: 1em;
    }
    .tarjeta h2 { margin-top: 0; }
    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
    }
    .descargar {
      margin-top: 1em;
      display: inline-block;
      padding: 0.5em 1em;
      background: #007acc;
      color: white;
      border-radius: 4px;
      text-decoration: none;
    }
    .modo {
      position: fixed;
      top: 1em;
      right: 1em;
      background: #ccc;
      border: none;
      padding: 0.5em 1em;
      border-radius: 4px;
      cursor: pointer;
    }
    :root {
      --bg: #f0f0f0;
      --fg: #000;
      --card-bg: #fff;
    }
    .oscuro {
      --bg: #121212;
      --fg: #eee;
      --card-bg: #1e1e1e;
    }
    .grupo {
      margin-top: 2em;
    }
    .grupo h1 {
      border-bottom: 2px solid #ccc;
    }
  </style>
</head>
<body id="body">
  <button class="modo" onclick="document.getElementById('body').classList.toggle('oscuro')">🌙/☀️</button>
  <h1>📋 Informes de revisión</h1>
'''

# Verificar informes
informes = [f for f in os.listdir("resultados") if f.endswith(".txt")]
os.makedirs("web/informes", exist_ok=True)

exitosos = []
fallidos = []

for archivo in informes:
    shutil.copy(f"resultados/{archivo}", f"web/informes/{archivo}")
    with open(f"resultados/{archivo}", "r", encoding="utf-8") as f:
        contenido = f.read()
    nombre = archivo.replace(".txt", "")
    tarjeta = f'''
    <div class="tarjeta">
      <h2>{nombre}.c</h2>
      <pre>{contenido}</pre>
      <a class="descargar" href="informes/{archivo}" download>Descargar informe</a>
    </div>
    '''
    if "✅ Compilación exitosa" in contenido:
        exitosos.append(tarjeta)
    else:
        fallidos.append(tarjeta)

if exitosos:
    html += f'<div class="grupo"><h1>✅ Exitosos ({len(exitosos)})</h1>'
    html += ''.join(exitosos) + '</div>'

if fallidos:
    html += f'<div class="grupo"><h1>❌ Con errores ({len(fallidos)})</h1>'
    html += ''.join(fallidos) + '</div>'

if not informes:
    html += "<p>No se encontraron informes en la carpeta <code>resultados/</code>.</p>"

html += '</body></html>'

os.makedirs("web", exist_ok=True)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
