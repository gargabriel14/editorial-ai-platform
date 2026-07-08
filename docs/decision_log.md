# Decision Log

## ADR-0001: Plataforma modular por servicios

- Estado: aprobada
- Decision: cada modulo del negocio expone un servicio independiente y usa
  modelos compartidos desde `core`.
- Motivo: permite cambiar fuentes de datos, proveedores de IA o automatizaciones
  sin reescribir el negocio.

## ADR-0002: SQLite para MVP local

- Estado: aprobada
- Decision: usar SQLite como base local de oportunidades y eventos.
- Motivo: suficiente para prototipo, facil de probar y compatible con n8n local.
- Migracion futura: PostgreSQL cuando haya concurrencia, usuarios o jobs en cola.

## ADR-0003: Dashboard web stdlib

- Estado: aprobada
- Decision: crear una web servida con `http.server` y JavaScript vanilla.
- Motivo: visualizacion inmediata sin dependencias frontend ni backend pesadas.
- Migracion futura: FastAPI + React/Vue/Svelte si el dashboard se vuelve producto.

## ADR-0004: CEO-CTO sync por repo, issues y n8n

- Estado: propuesta
- Decision: usar GitHub y `docs/decision_log.md` como memoria compartida entre
  CEO ChatGPT y CTO Codex.
- Motivo: las decisiones quedan auditables, versionadas y conectadas al codigo.

