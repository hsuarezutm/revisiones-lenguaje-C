import os

html = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe de Programas en C</title>
  <style>
    body { font-family: sans-serif; padding: 2em; transition: background 0.3s, color 0.3s; }
    .tarjeta {
      background: var(--card-bg); border-radius: 8px; padding: 1em;
      box-shadow: 0 0 10px rgba(0,0,0,0.1); margin-bottom: 1em;
    }
    .tarjeta h2 { margin-top: 0; }
    pre { white-space: pre-wrap; word-wrap: break-word; }
    .descargar {
      margin-top: 1em; display: inline-block; padding: 0.5em 1em;
      background: #007acc; color: white; border-radius: 4px; text-decoration: none;
    }
    .modo {
      position: fixed; top: 1em; right: 1em; background: #ccc; border: none;
      padding: 0.5em 1em; border-radius: 4px; cursor: pointer;
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
  </style>
</head>
<body id="body" style="background: var(--bg); color: var(--fg);">
  <button class="modo" onclick="document.getElementById('body').classList.toggle('oscuro')">🌙/☀️</button>
  <h1>📋 Informes de revisión</h1>
'''

for archivo in os.listdir("resultados"):
    if archivo.endswith(".txt"):
        nombre = archivo.replace(".txt", "")
        with open(f"resultados/{archivo}", "r", encoding="utf-8") as f:
            contenido = f.read()
        html += f'''
        <div class="tarjeta">
          <h2>{nombre}.c</h2>
          <pre>{contenido}</pre>
          <a class="descargar" href="../resultados/{archivo}" download>Descargar informe</a>
        </div>
        '''

html += '</body></html>'

os.makedirs("web", exist_ok=True)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
