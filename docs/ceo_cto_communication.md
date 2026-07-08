# Comunicacion CEO ChatGPT + CTO Codex

## Objetivo

Que el CEO IA y el CTO Codex compartan decisiones, contexto y estado operativo
sin depender de memoria informal de chats sueltos.

## Arquitectura recomendada

La fuente de verdad debe ser el repositorio:

- `docs/decision_log.md`: decisiones aprobadas y pendientes.
- GitHub Issues: preguntas estrategicas, aprobaciones y bloqueos.
- Pull Requests: cambios de producto, tests y justificacion tecnica.
- Web dashboard: estado vivo de oportunidades, SEO, estructura y marketing.
- n8n: resumenes programados, alertas y handoffs.

## Flujo CEO -> CTO

El CEO ChatGPT deberia enviar un decision packet:

```text
Contexto:
Objetivo:
Opciones:
Recomendacion:
Riesgos:
Decision requerida:
Fecha limite:
```

Codex convierte ese packet en cambios de repo, issues, automatizaciones o PRs.

## Flujo CTO -> CEO

Codex debe responder con:

```text
Cambio realizado:
Impacto en negocio:
Riesgos:
Pruebas ejecutadas:
Decision pendiente:
Siguiente accion recomendada:
```

## Automatizacion n8n sugerida

1. Cada dia, llamar a `GET /api/dashboard`.
2. Enviar resumen al CEO ChatGPT por el canal elegido.
3. Si hay oportunidades con score >= 70, abrir GitHub Issue.
4. Si el CEO aprueba, crear una tarea para Codex con el decision packet.
5. Al cerrar la tarea, Codex actualiza `docs/decision_log.md`.

## Por que esta arquitectura

El chat es bueno para razonar. El repositorio es mejor para recordar. GitHub es
mejor para auditar. n8n es mejor para repetir. Separar esos roles evita que la
empresa dependa de conversaciones perdidas.

