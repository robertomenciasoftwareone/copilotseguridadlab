---
name: explicar-hallazgo
description: "Explica un hallazgo de checkov o trivy para negocio y para técnicos, con la corrección exacta"
argument-hint: "identificador del hallazgo (CKV_..., AVD-..., KSV...) y fichero"
agent: ask
---

# Explicar un hallazgo de seguridad

Hallazgo: `${input:hallazgo:CKV_GCP_114}` en `${input:fichero:legacy/infra/bucket.tf}`.

Responde en cuatro bloques cortos:

1. **Qué significa** en una frase que entienda alguien de negocio.
2. **Qué podría pasar** en IGEO si no se corrige (un escenario concreto y creíble).
3. **La corrección exacta**: el bloque de código antes y después.
4. **Cómo evitar que vuelva**: qué línea de las instrucciones de Copilot del repositorio lo previene, o qué habría que añadir.
