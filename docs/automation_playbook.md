# Playbook de automatizacion

## Regla CTO

Toda tarea que se repita mas de dos veces y tenga entradas/salidas claras debe
ser candidata a automatizacion.

## Automatizaciones prioritarias

| Tarea | Trigger | Accion | Herramienta |
| --- | --- | --- | --- |
| Refresh de tendencias | Diario | Recolectar datos y re-scorear oportunidades | n8n + API |
| Oportunidad con score alto | Score >= 70 | Crear estructura, SEO pack y aviso al equipo | n8n |
| Produccion de manuscrito | Aprobacion humana | Crear tareas editoriales y assets base | n8n + gestor de proyectos |
| QA editorial | Manuscrito listo | Ejecutar checklist de calidad y originalidad | Pipeline interno |
| Lanzamiento | Fecha de publicacion | Enviar emails, posts y campanas | n8n |
| Analitica | Semanal | Importar ventas, ads y ranking | n8n + reportes |

## Workflow incluido

Archivo: `automations/n8n/opportunity_pipeline.workflow.json`

Funcion:

1. Se ejecuta cada 24 horas.
2. Llama a `POST /pipelines/opportunities/run`.
3. Si la mejor oportunidad tiene score >= 70, dispara una notificacion.
4. Si no, espera mas datos.

## Proxima mejora

Sustituir el nodo `noOp` de notificacion por Slack, email, Notion, Airtable o
el sistema real que use la editorial.

