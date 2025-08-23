import os
import shutil

# Preparar carpetas
informes = [f for f in os.listdir("resultados") if f.endswith(".txt")]
os.makedirs("web/informes", exist_ok=True)

# Clasificar informes
exitosos = []
fallidos = []

for archivo in informes:
    shutil.copy(f"resultados/{archivo}", f"web/informes/{archivo}")
    with open(f"resultados/{archivo}", "r", encoding="utf-8") as f:
        contenido = f.read()
    nombre = archivo.replace(".txt", "")
    tarjeta = f'''
    <div class="card">
      <h2>{nombre}.c</h2>
      <pre>{contenido}</pre>
      <a class="download" href="informes/{archivo}" download>📥 Descargar informe</a>
    </div>
    '''
    if "✅ Compilación exitosa" in contenido:
        exitosos.append(tarjeta)
    else:
        fallidos.append(tarjeta)

# Estadísticas
total = len(informes)
ok = len(exitosos)
fail = len(fallidos)
porcentaje = round((ok / total) * 100, 2) if total else 0

# HTML base
html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Dashboard de Revisión</title>
  <style>
    :root {{
      --bg: #f5f7fa;
      --fg: #222;
      --card-bg: #fff;
      --accent: #007acc;
    }}
    .dark {{
      --bg: #121212;
      --fg: #eee;
      --card-bg: #1e1e1e;
      --accent: #00bcd4;
    }}
    body {{
      background: var(--bg);
      color: var(--fg);
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 2em;
      transition: background 0.3s, color 0.3s;
    }}
    header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2em;
    }}
    h1 {{
      margin: 0;
    }}
    .toggle {{
      background: var(--accent);
      color: white;
      border: none;
      padding: 0.5em 1em;
      border-radius: 5px;
      cursor: pointer;
    }}
    .stats {{
      background: var(--card-bg);
      padding: 1em;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      margin-bottom: 2em;
    }}
    .stats p {{
      margin: 0.5em 0;
    }}
    .group {{
      margin-top: 2em;
    }}
    .group h2 {{
      border-bottom: 2px solid var(--accent);
    }}
    .card {{
      background: var(--card-bg);
      padding: 1em;
      border-radius: 8px;
      box-shadow: 0 0 5px rgba(0,0,0,0.1);
      margin-bottom: 1em;
    }}
    pre {{
      white-space: pre-wrap;
      word-wrap: break-word;
    }}
    .download {{
      display: inline-block;
      margin-top: 1em;
      background: var(--accent);
      color: white;
      padding: 0.5em 1em;
      border-radius: 4px;
      text-decoration: none;
    }}
  </style>
</head>
<body id="body">
  <header>
    <h1>📋 Dashboard de revisión</h1>
    <button class="toggle" onclick="document.getElementById('body').classList.toggle('dark')">🌙/☀️</button>
  </header>

  <div class="stats">
    <h2>📊 Resumen estadístico</h2>
    <p>Total de archivos revisados: <strong>{total}</strong></p>
    <p>Compilaciones exitosas: <strong>{ok}</strong></p>
    <p>Errores detectados: <strong>{fail}</strong></p>
    <p>Porcentaje de éxito: <strong>{porcentaje}%</strong></p>
  </div>
'''

# Tarjetas por grupo
if exitosos:
    html += '<div class="group"><h2>✅ Exitosos</h2>' + ''.join(exitosos) + '</div>'
if fallidos:
    html += '<div class="group"><h2>❌ Con errores</h2>' + ''.join(fallidos) + '</div>'
if not informes:
    html += "<p>No se encontraron informes en la carpeta <code>resultados/</code>.</p>"

html += '</body></html>'

# Guardar archivo
os.makedirs("web", exist_ok=True)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
