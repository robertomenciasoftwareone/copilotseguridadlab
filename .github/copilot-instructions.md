# Plataforma IGEO: seguridad por diseño

Este repositorio contiene la infraestructura (Terraform en Google Cloud), los manifiestos Kubernetes y los pipelines del **Visor IGEO**. La seguridad no es una revisión al final: es una condición para que el código exista.

## Idioma y forma de responder
- Responde siempre en español. Código y nombres de recursos en inglés, comentarios en español.
- Si una petición pide algo inseguro (acceso público, permisos amplios, secretos en código), **no lo generes tal cual**: explica el riesgo en una frase y propone la alternativa segura. Si de verdad hace falta, pide que se justifique y deja un comentario `# EXCEPCIÓN-SEGURIDAD: <motivo>`.

## Secretos (regla absoluta)
- Nunca escribas contraseñas, tokens, claves de API, claves privadas ni ficheros de credenciales en el repositorio, ni siquiera de ejemplo con formato real.
- Los secretos viven en **Secret Manager** (GCP) o en `Secret` de Kubernetes creados fuera del repositorio. En el código se referencian por nombre.
- En ejemplos usa el marcador `<SECRETO-EN-SECRET-MANAGER>`.
- Si encuentras un secreto en el código, avisa: hay que **revocarlo y rotarlo**, borrarlo del fichero no basta porque sigue en el historial de git.

## Mínimo privilegio
- Ningún permiso con comodines (`*`), ningún rol básico de GCP (owner, editor, viewer), ningún `allUsers` ni `allAuthenticatedUsers`.
- Cada carga de trabajo, su propia identidad (cuenta de servicio de GCP o ServiceAccount de Kubernetes) con solo los permisos que usa.

## Cómo se valida (obligatorio antes de dar algo por terminado)
- Secretos: `gitleaks dir <carpeta> -c .gitleaks.toml`
- Infraestructura y Kubernetes: `checkov -d <carpeta> --compact --quiet` y `trivy config <carpeta>`.
- No des una tarea por terminada con hallazgos HIGH o CRITICAL abiertos. Si uno no aplica, márcalo con su supresión explicada (`#checkov:skip=CKV_...:motivo`).

## Lo que nunca haces
- Nunca `git push --force`, nunca `git commit --no-verify`, nunca desactivar un escáner para que el pipeline pase.
- Nunca cambies `.github/` (instrucciones, agentes, hooks, workflows) sin decirlo explícitamente: son controles de seguridad y los revisa el equipo de plataforma (CODEOWNERS).
