# Política de uso de GitHub Copilot

## 1. Objetivo y alcance

Establecer un uso seguro y responsable de GitHub Copilot en IGEO. Esta política
aplica a las personas con licencia de los equipos de plataforma, desarrollo y
datos, y cubre el chat, las sugerencias, los modelos y agentes, incluidos el
agente de codificación en la nube y los servidores MCP.

## 2. Qué se puede y qué no se puede hacer

| Se puede | No se puede |
|---|---|
| Solicitar explicaciones o propuestas usando contexto autorizado. | Pegar secretos, datos personales o información confidencial en un chat. |
| Usar modelos aprobados y servidores MCP de la lista blanca. | Usar modelos o servidores MCP no aprobados. |
| Probar y adaptar código sugerido antes de proponerlo. | Fusionar código generado sin revisión humana ni controles de seguridad. |
| Participar en el piloto del agente en la nube en los dos repositorios autorizados. | Utilizar el agente en la nube fuera del piloto autorizado. |

## 3. Datos y confidencialidad

Nunca se pegan en el chat contraseñas, tokens, claves, credenciales, datos
personales ni información confidencial. Usá datos anonimizados o ficticios sin
formato de credencial real y compartí solo el contexto necesario.

La exclusión de contenido comprende `secrets/`, `**/*.pem`, `**/.env*` y el
repositorio `igeo-datos-personales`. En modo agente, la exclusión bloquea el
acceso mediante herramientas de Copilot y comprueba rutas identificables en
comandos, pero puede no detectar accesos indirectos. Tampoco garantiza que
clientes o servidores MCP de terceros la respeten, ni sustituye los permisos
del sistema. El IDE podría proporcionar información semántica indirecta.

## 4. Seguridad del código generado

La persona que propone un cambio debe revisarlo y verificarlo: Copilot no
sustituye el criterio humano. Toda fusión requiere revisión humana y la
ejecución de gitleaks, checkov y trivy en cada pull request. Push protection está
activado en todos los repositorios.

Los secretos se gestionan fuera del código, mediante Secret Manager o `Secret`
de Kubernetes creados fuera del repositorio. Si se detecta una credencial
expuesta, hay que revocarla y rotarla: borrarla no elimina su historial.
Los cambios en `.github/` requieren revisión del equipo de plataforma.

## 5. Propiedad intelectual y licencias

El filtro de sugerencias coincidentes con código público está configurado en
**Bloquear**, indicado como requisito para la indemnización de propiedad
intelectual. Las referencias de código están activadas en el agente de GitHub
para mostrar la licencia del código coincidente. Antes de incorporar una
dependencia o contenido de terceros, revisá sus condiciones de licencia; el
filtro no sustituye esa revisión. La indemnización de propiedad intelectual
depende de sus condiciones contractuales aplicables.

## 6. Configuración de la organización

| Política | Valor | Motivo |
|---|---|---|
| Plan | GitHub Copilot Business | Plan indicado para la organización. |
| Sugerencias coincidentes con código público | Bloquear | Reducir riesgos de propiedad intelectual. |
| Referencias de código | Activadas en el agente de GitHub | Mostrar la licencia de coincidencias. |
| Modelos | Aprobados por el comité de arquitectura; revisión trimestral | Mantener control sobre los modelos utilizados. |
| Servidores MCP | Solo los de la lista blanca del repositorio de plataforma | Limitar integraciones no autorizadas. |
| Agente en la nube | Piloto en dos repositorios | Limitar el alcance inicial. |
| Exclusión de contenido | Rutas y repositorio indicados en la sección 3 | Reducir exposición de datos sensibles. |
| Revisión y escáneres | Revisión humana, gitleaks, checkov y trivy en cada pull request; push protection | Detectar riesgos antes de integrar cambios. |
| Cambios en `.github/` | Revisión de plataforma mediante CODEOWNERS | Proteger los controles de seguridad. |
| Auditoría de Copilot | Revisión mensual por seguridad | Supervisar el uso. |

## 7. Licencias de Copilot

Las licencias se destinan a los equipos de plataforma, desarrollo y datos.
Se solicitan por el portal de servicios con el visto bueno de la persona
responsable del equipo y se retiran tras 45 días sin uso. Antes de recibir
una licencia es obligatorio completar el programa de formación de cuatro sesiones.

El consumo adicional tiene un tope mensual y una alerta al 80 %; dirección
de sistemas es responsable de su control.

> Pendiente de decidir: ¿se ha confirmado con GitHub que los créditos mensuales
> incluidos en las licencias forman un fondo común para toda la organización,
> como indican los datos facilitados?

## 8. Responsables y revisión

> Pendiente de decidir: ¿quién mantiene y aprueba esta política?

> Pendiente de decidir: ¿con qué frecuencia se revisa esta política?
