---
name: "Kubernetes seguro IGEO"
description: "RBAC restrictivo, identidades por carga de trabajo y seguridad de pods"
applyTo: "k8s/**/*.yaml,k8s/**/*.yml"
---

# Kubernetes seguro (normas de ejemplo de IGEO)

## RBAC (quién puede hacer qué dentro del clúster)
- **Role y RoleBinding con namespace**, no ClusterRole ni ClusterRoleBinding, salvo justificación escrita.
- **Prohibidos los comodines**: nada de `"*"` en `apiGroups`, `resources` ni `verbs`. Enumera exactamente los recursos y verbos que se usan.
- **Nunca** enlazar `cluster-admin`, `admin` ni `edit`.
- Prohibidos los verbos `escalate`, `bind` e `impersonate`, y el recurso `pods/exec`.
- `secrets`: solo si es imprescindible, con `resourceNames` concretos y solo `get`. Nunca `list` ni `watch` sobre secrets.
- Cada `RoleBinding` apunta a una **ServiceAccount dedicada** (nunca a `default`).

## ServiceAccount
- Una por aplicación o pipeline, con `automountServiceAccountToken: false` salvo que la aplicación hable con la API de Kubernetes.

## Pods
- `runAsNonRoot: true`, `runAsUser` numérico, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`, `capabilities.drop: ["ALL"]`, `seccompProfile: RuntimeDefault`.
- Imagen con versión fija o digest, `requests` y `limits.memory`, sondas de readiness y liveness.

## Validación
- `checkov -d <carpeta> --framework kubernetes --compact --quiet` y `trivy config <carpeta>` sin HIGH ni CRITICAL.
