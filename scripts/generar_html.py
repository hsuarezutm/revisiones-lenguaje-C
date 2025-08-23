import os

html = '''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Informe de Programas en C</title>
</head>
<body>
  <h1>📋 Informes de revisión</h1>
'''

for archivo in os.listdir("resultados"):
    if archivo.endswith(".txt"):
        nombre = archivo.replace(".txt", "")
        with open(f"resultados/{archivo}", "r", encoding="utf-8") as f:
            contenido = f.read()
        html += f'''
        <div>
          <h2>{nombre}.c</h2>
          <pre>{contenido}</pre>
        </div>
        '''

html += '</body></html>'

os.makedirs("web", exist_ok=True)
with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(html)
