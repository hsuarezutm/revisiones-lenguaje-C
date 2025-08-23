import os
import shutil
import zipfile

# Preparar carpetas
informes = [f for f in os.listdir("resultados") if f.endswith(".txt")]
os.makedirs("web/informes", exist_ok=True)

# Copiar informes y crear ZIP
with zipfile.ZipFile("web/informes.zip", "w") as zipf:
    for archivo in informes:
        src = f"resultados/{archivo}"
        dst = f"web/informes/{archivo}"
        shutil.copy(src, dst)
        zipf.write(dst, arcname=archivo)

# Clasificar
exitosos, advertencias, errores = [], [], []
tabla = ""

for archivo in informes:
    with open(f"resultados/{archivo}", "r", encoding="utf-8") as f:
        contenido = f.read()
    nombre = archivo.replace(".txt", "")
    tarjeta = f'''
    <div class="card" data-nombre="{nombre}" data-estado="{contenido[:2]}">
      <h2>{nombre}.c</h2>
      <pre>{contenido}</pre>
      <a class="download" href="informes/{archivo}" download>📥 Descargar informe</a>
    </div>
    '''
    if "✅" in contenido:
        exitosos.append(tarjeta)
        estado = "✅"
    elif "⚠️" in contenido:
        advertencias.append(tarjeta)
        estado = "⚠️"
    else:
        errores.append(tarjeta)
        estado = "❌"
    fila = f"<tr><td>{nombre}.c</td><td>{estado}</td><td><a href='informes/{archivo}' download>📥</a></td></tr>"
    tabla += fila

# Estadísticas
total = len(informes)
ok = len(exitosos)
warn = len(advertencias)
fail = len(errores)
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
    .stats, .group {{
      background: var(--card-bg);
      padding: 1em;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
      margin-bottom: 2em;
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
    .search, .filters {{
      margin-bottom: 1em;
    }}
    input[type="text"] {{
      padding: 0.5em;
      width: 100%;
      max-width: 400px;
      border: 1px solid #ccc;
      border-radius: 4px;
    }}
    .filters button {{
      margin-right: 0.5em;
      padding: 0.4em 0.8em;
      border: none;
      background: var(--accent);
      color: white;
      border-radius: 4px;
      cursor: pointer;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
    }}
    th, td {{
      padding: 0.5em;
      border-bottom: 1px solid #ccc;
      text-align: left;
    }}
    .actions {{
      margin-top: 1em;
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
    <p>Advertencias: <strong>{warn}</strong></p>
    <p>Errores detectados: <strong>{fail}</strong></p>
    <p>Porcentaje de éxito: <strong>{porcentaje}%</strong></p>
    <div class="actions">
      <a class="download" href="informes.zip" download>📦 Descargar todos (.zip)</a>
      <button class="download" onclick="window.print()">🧾 Exportar como PDF</button>
    </div>
  </div>

  <div class="search">
    <input type="text" id="busqueda" placeholder="🔍 Buscar por nombre...">
  </div>

  <div class="filters">
    <button onclick="filtrarEstado('')">Todos</button>
    <button onclick="filtrarEstado('✅')">Exitosos</button>
    <button onclick="filtrarEstado('⚠️')">Advertencias</button>
    <button onclick="filtrarEstado('❌')">Errores</button>
  </div>

  <div class="group">
    <h2>📋 Tabla resumen</h2>
    <table>
      <thead><tr><th>Archivo</th><th>Estado</th><th>Informe</th></tr></thead>
      <tbody>{tabla}</tbody>
    </table>
  </div>
'''

# Tarjetas por grupo
if exitosos:
    html += '<div class="group"><h2 id="exitosos">✅ Exitosos</h2>' + ''.join(exitosos) + '</div>'
if advertencias:
    html += '<div class="group"><h2 id="advertencias">⚠️ Advertencias</h2>' + ''.join(advertencias) + '</div>'
if errores:
    html += '<div class="group"><h2 id="errores">❌ Errores</h2>' + ''.join(errores) + '</div>'
if not informes:
    html += "<p>No se encontraron informes en la carpeta <code>resultados/</code>.</p>"

# Cierre con script funcional
html += '''
<script>
document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("busqueda");
  const tarjetas = document.querySelectorAll(".card");

  input.addEventListener("input", function () {
    const texto = input.value.toLowerCase();
    tarjetas.forEach(t => {
      const nombre = t.getAttribute("data-nombre")?.toLowerCase() || "";
      t.style.display = nombre.includes(texto) ? "block" : "none";
    });
  });
});

function filtrarEstado(estado) {
  const tarjetas = document.querySelectorAll(".card");
  tarjetas.forEach(t => {
    const tipo = t.getAttribute("data-estado") || "";
    t.style.display = (estado === "" || tipo === estado) ? "block" : "none";
  });
}
</script>
</body></html>
'''

# Guardar archivo
os.makedirs("web", exist_ok=True)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
