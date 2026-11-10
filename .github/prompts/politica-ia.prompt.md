---
name: politica-ia
description: "Redacta la política de uso de GitHub Copilot de la organización a partir de sus datos"
argument-hint: "fichero de datos (por defecto docs/gobernanza/datos-organizacion.md)"
agent: agent
tools: ['read', 'edit']
---

# Política de uso de GitHub Copilot

Lee `${input:datos:docs/gobernanza/datos-organizacion.md}` y redacta `docs/gobernanza/POLITICA-USO-COPILOT.md` con estas secciones, en este orden y en español claro (máximo dos páginas):

1. **Objetivo y alcance**: a quién aplica y qué herramientas cubre.
2. **Qué se puede y qué no se puede hacer**: tabla de dos columnas con ejemplos concretos.
3. **Datos y confidencialidad**: qué no se pega nunca en un chat, exclusión de contenido y su limitación en modo agente.
4. **Seguridad del código generado**: revisión humana obligatoria, escáneres del pipeline, secretos.
5. **Propiedad intelectual y licencias**: filtro de código público, referencias de código, licencias de terceros.
6. **Configuración de la organización**: tabla `política · valor · motivo` con lo que indique el fichero de datos.
7. **Licencias de Copilot**: quién recibe licencia, cómo se pide, cuándo se retira por inactividad y cómo se controla el consumo.
8. **Responsables y revisión**: quién mantiene la política y cada cuánto se revisa.

No inventes datos de la organización: si falta algo, escribe `> Pendiente de decidir:` y la pregunta concreta.
