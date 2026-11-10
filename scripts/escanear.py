"""Pasa los tres escáneres de seguridad sobre una carpeta y resume el resultado.

Uso:
    python scripts/escanear.py legacy          # el "antes"
    python scripts/escanear.py infra k8s       # lo generado
    python scripts/escanear.py reto            # el reto final

  gitleaks  -> secretos en ficheros
  checkov   -> malas configuraciones en Terraform y Kubernetes (más de 1.000 reglas)
  trivy     -> malas configuraciones y secretos (otro motor, otras reglas)

Sale con código 1 si algún escáner encuentra algo. Funciona sin Internet salvo
la primera ejecución de trivy, que descarga sus reglas.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ejecutar(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=RAIZ, check=False)


def gitleaks(rutas: list[str]) -> list[str]:
    hallazgos = []
    for ruta in rutas:
        informe = os.path.join(RAIZ, ".gitleaks-informe.json")
        ejecutar(["gitleaks", "dir", ruta, "--no-banner", "--redact", "--report-format", "json",
                  "--report-path", informe, "-c", os.path.join(RAIZ, ".gitleaks.toml")])
        if os.path.exists(informe):
            with open(informe, encoding="utf-8") as f:
                for h in json.load(f) or []:
                    hallazgos.append(f"{h['File']}:{h['StartLine']}  {h['RuleID']}")
            os.remove(informe)
    return hallazgos


def checkov(rutas: list[str]) -> list[str]:
    hallazgos = []
    for ruta in rutas:
        res = ejecutar(["checkov", "--quiet", "--compact", "-o", "json", "--framework", "terraform", "kubernetes", "-d", ruta])
        try:
            datos = json.loads(res.stdout or "[]")
        except json.JSONDecodeError:
            hallazgos.append(f"(no se pudo leer la salida de checkov) {res.stderr[-300:]}")
            continue
        for b in datos if isinstance(datos, list) else [datos]:
            for c in (b.get("results") or {}).get("failed_checks", []):
                rel = c["file_path"].lstrip("/")
                fichero = rel if rel.startswith(ruta.rstrip("/") + "/") else ruta.rstrip("/") + "/" + rel
                hallazgos.append(f"{fichero}:{c['file_line_range'][0]}  {c['check_id']}  {c['check_name']}")
    return hallazgos


def ignorar_trivy() -> list[str]:
    fichero = os.path.join(RAIZ, ".trivyignore.yaml")
    return ["--ignorefile", fichero] if os.path.exists(fichero) else []


def trivy(rutas: list[str]) -> list[str]:
    hallazgos = []
    for ruta in rutas:
        res = ejecutar(["trivy", "fs", "--scanners", "misconfig,secret", "--severity", "HIGH,CRITICAL",
                        "--format", "json", "--quiet", *ignorar_trivy(), ruta])
        try:
            datos = json.loads(res.stdout or "{}")
        except json.JSONDecodeError:
            hallazgos.append(f"(no se pudo leer la salida de trivy) {res.stderr[-300:]}")
            continue
        for r in datos.get("Results") or []:
            for m in r.get("Misconfigurations") or []:
                hallazgos.append(f"{ruta.rstrip('/')}/{r['Target']}  {m['ID']}  {m['Severity']}  {m['Title']}")
            for s in r.get("Secrets") or []:
                hallazgos.append(f"{ruta.rstrip('/')}/{r['Target']}:{s['StartLine']}  secreto  {s['Severity']}  {s['Title']}")
    return hallazgos


def main(argv: list[str]) -> int:
    rutas = argv or ["infra", "k8s"]
    rutas = [r for r in rutas if os.path.exists(os.path.join(RAIZ, r))]
    if not rutas:
        print("No hay nada que escanear en esas rutas.")
        return 0
    total = 0
    for nombre, funcion in (("gitleaks (secretos)", gitleaks), ("checkov (IaC y Kubernetes)", checkov),
                            ("trivy (configuración y secretos, HIGH/CRITICAL)", trivy)):
        binario = nombre.split()[0]
        print(f"\n== {nombre} ==")
        if not shutil.which(binario):
            print(f"  {binario} no está instalado: se omite")
            continue
        hallazgos = funcion(rutas)
        for h in hallazgos:
            print("  " + h)
        print(f"  -> {len(hallazgos)} hallazgo(s)")
        total += len(hallazgos)
    print(f"\nRESULTADO: {'NO APTO' if total else 'APTO'} ({total} hallazgos en {', '.join(rutas)})")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
