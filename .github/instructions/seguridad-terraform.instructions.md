---
name: "Terraform seguro IGEO"
description: "Seguridad por diseño en Terraform para Google Cloud: buckets privados, IAM mínimo, red y cifrado"
applyTo: "**/*.tf,**/*.tfvars"
---

# Terraform seguro en Google Cloud (normas de ejemplo de IGEO)

## Buckets de Cloud Storage (`google_storage_bucket`)
- **Siempre**: `public_access_prevention = "enforced"` y `uniform_bucket_level_access = true`. Un bucket no puede ser público ni por error.
- `versioning { enabled = true }`, `force_destroy = false` y `logging` hacia el bucket de auditoría (`var.bucket_logs`).
- Región explícita de la UE (`europe-southwest1` por defecto), nunca multirregión fuera de la UE.
- Cifrado con clave gestionada (CMEK) cuando el dato sea personal o sensible: `encryption { default_kms_key_name = var.kms_key }`.
- Si alguien necesita leer desde fuera: URL firmadas de corta duración, o un grupo concreto con `roles/storage.objectViewer`. **Nunca** `allUsers` ni `allAuthenticatedUsers`.

## IAM
- Solo `google_*_iam_member` con roles predefinidos. Prohibidos `roles/owner`, `roles/editor`, `roles/viewer`.
- Miembros: grupos (`group:`) o cuentas de servicio dedicadas (`serviceAccount:`). Nunca personas sueltas (`user:`) para permisos permanentes.
- Ninguna clave de cuenta de servicio (`google_service_account_key`): se usa Workload Identity.

## Red
- Ninguna regla de firewall con `0.0.0.0/0` hacia puertos de administración (22, 3389). Acceso administrativo por IAP (`35.235.240.0/20`).

## Secretos
- Ningún secreto en variables con `default` ni en `.tfvars`. Secretos con `google_secret_manager_secret`; el valor se carga fuera de Terraform.

## Validación
- `checkov -d <carpeta> --framework terraform --compact --quiet` y `trivy config <carpeta>` sin HIGH ni CRITICAL.
