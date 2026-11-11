---
name: auditar-secretos
description: "Busca secretos con gitleaks y explica cada hallazgo y qué hacer con él"
argument-hint: "carpeta (por defecto legacy)"
agent: agent
tools: ['read', 'search', 'execute']
---

# Auditar secretos

1. Ejecuta desde la raíz del repositorio `gitleaks dir ${input:carpeta:legacy} -v --redact -c .gitleaks.toml` (el `-c` es imprescindible: sin él gitleaks no usa nuestra regla de contraseñas).
2. Lee además los ficheros de esa carpeta y busca lo que gitleaks no detecta (contraseñas en comentarios, URLs con usuario y contraseña, credenciales en texto libre).
3. Devuelve SOLO esta tabla:

| # | Fichero:línea | Tipo de secreto | ¿Lo detectó gitleaks? | Riesgo (una frase) | Acción: revocar/rotar · mover a Secret Manager · referencia que debe quedar en el código |

4. Termina con un párrafo de tres líneas: por qué borrar el secreto del fichero no basta y qué pasos hay que dar hoy.

No modifiques ningún fichero. No repitas el valor completo de ningún secreto: muestra solo los 4 primeros caracteres seguidos de `…`.
