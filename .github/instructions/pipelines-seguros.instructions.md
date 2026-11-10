---
name: "Pipelines seguros IGEO"
description: "Cadena de suministro en GitHub Actions: acciones fijadas por SHA, permisos mínimos y escáneres de seguridad"
applyTo: ".github/workflows/**,.github/dependabot.yml"
---

# Pipelines seguros (normas de ejemplo de IGEO)

- **Toda acción de terceros fijada por el SHA completo del commit**, con la versión en un comentario: `uses: aquasecurity/trivy-action@<sha-40-caracteres> # v0.36.0`. Una etiqueta (`@v1`, `@master`) se puede mover; un SHA no.
- `dependabot.yml` con el ecosistema `github-actions` para que los SHA se actualicen con pull requests revisadas.
- `permissions: contents: read` a nivel de workflow. Solo el job que sube resultados a Code Scanning pide `security-events: write`.
- Escáneres obligatorios en cada pull request: gitleaks (secretos), checkov (IaC y Kubernetes) y trivy (configuración y secretos). Resultados en formato SARIF subidos con `github/codeql-action/upload-sarif`.
- El pipeline falla con hallazgos HIGH o CRITICAL. Prohibido `continue-on-error: true` o `soft_fail: true` en los pasos que deciden.
- Ningún secreto impreso en el log ni pasado por línea de comandos. Autenticación en la nube solo con Workload Identity Federation.
