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

## ADR-0006: KDP Launch & Brand Readiness

- Estado: aprobada
- Issue CEO: #2
- Decision: cada oportunidad editorial debe evaluarse tambien como activo KDP,
  incluyendo tipo de libro, marca editorial, serie, metadata, lanzamiento,
  compliance y recomendacion accionable.
- Motivo: un nicho con buen score general puede fallar si no tiene estrategia de
  serie, diferenciacion, compliance de resenas o metadata KDP defendible.
- Scoring: demanda 20%, competencia 15%, serie 15%, produccion 10%, marca 15%,
  lanzamiento 10%, automatizacion 10% y compliance 5%.
- Guardrail: no aprobar piloto sin serie o producto complementario, salvo
  justificacion comercial fuerte documentada.
- Fuentes revisadas: Amazon KDP Content Guidelines, Customer Reviews, KDP
  Categories y Metadata Guidelines.

