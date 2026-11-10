# IGEO · Laboratorio Copilot · Sesión 4: Seguridad, gobernanza y licenciamiento

Repositorio listo para la demo. Todo funciona en un portátil. Las normas y los valores son **de ejemplo**: cada organización pone los suyos.

## Estructura

| Carpeta o fichero | Para qué sirve |
| --- | --- |
| `.github/copilot-instructions.md` | Reglas generales: secretos, mínimo privilegio, cómo se valida |
| `.github/instructions/` | Seguridad por diseño en Terraform (buckets privados, IAM), Kubernetes (RBAC restrictivo) y pipelines (acciones fijadas por SHA) |
| `.github/agents/` | `seguridad-implementer` (genera y escanea hasta verde) y `seguridad-revisor` (solo lee) |
| `.github/prompts/` | `/auditar-secretos`, `/explicar-hallazgo`, `/politica-ia` |
| `.github/hooks/` + `scripts/hooks/` | Bloquean que el agente escriba secretos o salte controles; tras cada edición pasan checkov |
| `.githooks/pre-commit` | Hook de **git**: gitleaks antes de cada commit (`git config core.hooksPath .githooks`) |
| `.gitleaks.toml` | Reglas de gitleaks: las de serie más una propia para contraseñas |
| `legacy/` | Configuración, Terraform y RBAC heredados con fallos **deliberados** (secretos falsos incluidos) |
| `reto/` | El reto final: 9 problemas escondidos |
| `infra/`, `k8s/` | Vacías: aquí genera Copilot en directo |
| `docs/gobernanza/datos-organizacion.md` | Datos de ejemplo para generar la política de uso de Copilot |
| `scripts/escanear.py` | Pasa gitleaks, checkov y trivy y resume: `python scripts/escanear.py legacy` |

## Requisitos del portátil del formador

```powershell
winget install --id Git.Git
winget install --id Python.Python.3.12
winget install --id Gitleaks.Gitleaks
winget install --id AquaSecurity.Trivy
pip install checkov
```

Ajustes de usuario de VS Code (JSON):

```json
{
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  "chat.useCustomAgentHooks": true,
  "chat.tools.terminal.enableAutoApprove": true,
  "chat.tools.terminal.autoApprove": {
    "/^gitleaks (dir|git)\\b/": true,
    "/^checkov\\b/": true,
    "/^trivy (config|fs)\\b/": true,
    "/^python scripts\\/escanear\\.py\\b/": true
  }
}
```

## Antes de cada ensayo

```bash
git config core.hooksPath .githooks                           # activa el pre-commit (una vez por clon)
git reset --hard && git clean -fd                             # volver al inicio
python scripts/escanear.py legacy                             # debe salir NO APTO
```

La solución completa (bucket seguro, RBAC mínimo, workflow de seguridad con acciones fijadas por SHA, CODEOWNERS, dependabot, política de uso y soluciones del reto) está en `plan-b/`, **fuera** de este repositorio a propósito.

> Los secretos de `legacy/` son falsos y no tienen formato de ningún proveedor: GitHub no bloquea su subida, pero gitleaks sí los detecta. Es intencionado.
