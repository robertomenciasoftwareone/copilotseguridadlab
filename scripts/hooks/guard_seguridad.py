"""Hook PreToolUse de IGEO: antes de cada acción del agente de Copilot.

1. Si el agente va a ESCRIBIR algo que parece un secreto (token, clave, contraseña),
   se bloquea: el secreto nunca llega al disco ni al historial de git.
2. Si va a EJECUTAR un comando que salta un control de seguridad o cambia la nube,
   se bloquea.

VS Code envía el evento como JSON por stdin. Código 2 = bloquear; el texto de
stderr llega al modelo, que lo lee y corrige su propuesta.
"""
from __future__ import annotations

import json
import re
import sys

SECRETOS = [
    ("un token de GitHub", re.compile(r"\b(gh[pousr]_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{60,})\b")),
    ("una clave de API de Google", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("una clave de acceso de AWS", re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("una clave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("una clave de cuenta de servicio de GCP", re.compile(r'"private_key_id"\s*:\s*"[a-f0-9]{20,}"')),
    ("un token de Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("una contraseña o clave en claro", re.compile(
        r"(?i)\b(?P<nombre>[a-z_.]*(password|passwd|pwd|secret|token|api_?key|clave)[a-z_]*)\s*[:=]\s*[\"']?"
        r"(?!os\.|process\.env|getenv|var\.|data\.|module\.|local\.|secrets\.|env\.|vars\.)"
        r"(?P<valor>[^\"'\s$<{(\[/]{8,})(?=[\"'\s,;]|$)")),
]

COMANDOS = [
    (re.compile(r"--no-verify\b|\bgit\s+commit\b.*\s-n\b"), "saltarse el pre-commit (--no-verify) desactiva el escáner de secretos"),
    (re.compile(r"\bgit\s+config\b.*core\.hooksPath"), "cambiar core.hooksPath desactiva los hooks de git del equipo"),
    (re.compile(r"\bgit\s+push\b.*(--force|-f\b)"), "git push --force reescribe el historial compartido"),
    (re.compile(r"--soft-fail|--exit-code\s+0\b|continue-on-error"), "un escáner que no puede fallar no protege"),
    (re.compile(r"\bgcloud\b.*\b(delete|set-iam-policy|add-iam-policy-binding|remove-iam-policy-binding|keys\s+create)\b"),
     "gcloud que borra, cambia IAM o crea claves lo ejecuta una persona"),
    (re.compile(r"\bkubectl\b.*\b(delete|create\s+(clusterrolebinding|secret))\b"), "kubectl que borra o crea permisos/secretos lo ejecuta una persona"),
    (re.compile(r"\bterraform\s+(apply|destroy)\b"), "terraform apply/destroy va por pipeline con plan revisado"),
]


REFERENCIA = re.compile(r"(?i)_(name|file|path|ref|id|env|arn|uri|url)$")


def parece_secreto(m: re.Match) -> bool:
    """Para la regla genérica: descarta referencias (DB_PASSWORD_NAME) y valores sin pinta de clave."""
    if "nombre" not in m.re.groupindex:
        return True
    if REFERENCIA.search(m.group("nombre")):
        return False
    valor = m.group("valor")
    clases = sum(bool(re.search(p, valor)) for p in (r"[a-z]", r"[A-Z]", r"[0-9]", r"[^A-Za-z0-9]"))
    return clases >= 3


def textos(valor) -> list[str]:
    """Todas las cadenas que contiene la entrada de la herramienta."""
    if isinstance(valor, str):
        return [valor]
    if isinstance(valor, dict):
        return [t for v in valor.values() for t in textos(v)]
    if isinstance(valor, list):
        return [t for v in valor for t in textos(v)]
    return []


def es_comando(evento: dict, entrada: dict) -> str:
    herramienta = str(evento.get("tool_name", evento.get("toolName", ""))).lower()
    comando = entrada.get("command", "") if isinstance(entrada, dict) else ""
    if not comando and any(p in herramienta for p in ("terminal", "run", "exec", "shell", "bash")):
        comando = " ".join(textos(entrada))
    return comando


def motivo_bloqueo(evento: dict) -> str | None:
    entrada = evento.get("tool_input", evento.get("toolArgs", {})) or {}
    comando = es_comando(evento, entrada)
    if comando:
        for patron, motivo in COMANDOS:
            if patron.search(comando):
                return f"{motivo}. Propón el comando y que lo decida una persona"
    for texto in textos(entrada):
        for nombre, patron in SECRETOS:
            if any(parece_secreto(m) for m in patron.finditer(texto)):
                return (f"ibas a escribir {nombre}. Los secretos no se escriben nunca en ficheros ni comandos: "
                        "usa la referencia <SECRETO-EN-SECRET-MANAGER> o una variable de entorno, "
                        "y si el secreto es real, hay que revocarlo y rotarlo")
    return None


def main() -> int:
    try:
        evento = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    motivo = motivo_bloqueo(evento)
    if motivo:
        print("BLOQUEADO por la política de seguridad de IGEO: " + motivo + ".", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
