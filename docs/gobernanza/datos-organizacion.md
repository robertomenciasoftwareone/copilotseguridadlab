# Datos de la organización para la política de uso de Copilot (normas de ejemplo)

> Valores de ejemplo para el laboratorio. Cada organización pone los suyos.

- Organización: IGEO. Personas con acceso a Copilot: equipos de plataforma, desarrollo y datos (unas 40 personas).
- Plan: GitHub Copilot Business. Cada licencia incluye créditos de IA mensuales compartidos en un fondo común de la organización.
- Presupuesto de consumo adicional: tope mensual con alerta al 80 %. Responsable: dirección de sistemas.
- Licencias: se piden por el portal de servicios con el visto bueno del responsable del equipo. Se retiran tras 45 días sin uso.
- Filtro de sugerencias que coinciden con código público: Bloquear (requisito para la indemnización de propiedad intelectual).
- Referencias de código: activadas en el agente de GitHub (muestra la licencia del código coincidente).
- Modelos permitidos: los que apruebe el comité de arquitectura; lista revisada cada trimestre.
- Servidores MCP: solo los de la lista blanca del repositorio de plataforma.
- Agente en la nube de Copilot (coding agent): piloto en dos repositorios.
- Exclusión de contenido: carpetas `secrets/`, `**/*.pem`, `**/.env*` y el repositorio `igeo-datos-personales`.
- Seguridad: revisión humana obligatoria antes de fusionar; gitleaks, checkov y trivy en cada pull request; push protection activado en todos los repositorios.
- Cambios en `.github/` (instrucciones, agentes, hooks, workflows): los aprueba el equipo de plataforma (CODEOWNERS).
- Registro de auditoría de Copilot: revisión mensual por el equipo de seguridad.
- Formación obligatoria antes de recibir licencia: este programa de cuatro sesiones.
- Responsable de la política: (sin decidir)
- Frecuencia de revisión de la política: (sin decidir)
