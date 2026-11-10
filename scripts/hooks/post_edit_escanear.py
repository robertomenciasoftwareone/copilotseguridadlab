"""Hook PostToolUse de IGEO: tras cada edición del agente, escanea lo que ha tocado.

Si el agente ha creado o cambiado un .tf o un YAML de Kubernetes (fuera de
legacy/ y reto/, que están mal a propósito), pasa checkov sobre esos ficheros.
Si hay hallazgos, sale con código 2: el resultado vuelve al modelo y lo corrige
en la siguiente iteración, sin que nadie se lo pida.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

EXCLUIDOS = ("legacy/", "reto/", "ab/")
RUTA = re.compile(r"[\w./\\:-]+\.(?:tf|ya?ml)\b")


def ficheros_tocados(evento: dict, raiz: str) -> list[str]:
    texto = json.dumps(evento.get("tool_input", {}), ensure_ascii=False).replace("\\\\", "/")
    rutas = []
    for r in set(RUTA.findall(texto)):
        absoluta = r if os.path.isabs(r) or re.match(r"^[A-Za-z]:/", r) else os.path.join(raiz, r)
        relativa = os.path.relpath(absoluta, raiz).replace("\\", "/")
        if relativa.startswith("..") or relativa.startswith(EXCLUIDOS) or relativa.startswith(".github/"):
            continue
        if os.path.isfile(absoluta):
            rutas.append(absoluta)
    return sorted(rutas)


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    raiz = evento.get("cwd") or os.getcwd()
    ficheros = ficheros_tocados(evento, raiz)
    if not ficheros or not shutil.which("checkov"):
        return 0
    cmd = ["checkov", "--compact", "--quiet", "--framework", "terraform", "kubernetes"]
    for f in ficheros:
        cmd += ["-f", f]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0 and "FAILED" in res.stdout:
        print("Escáner de seguridad (checkov) con hallazgos en lo que acabas de escribir. "
              "Corrígelos antes de seguir:\n" + res.stdout[-4000:], file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
