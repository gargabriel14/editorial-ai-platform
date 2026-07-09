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

## ADR-0005: n8n local con Docker Compose

- Estado: aprobada
- Decision: ejecutar n8n localmente con Docker Compose desde `infra/n8n`,
  persistiendo datos y credenciales en el volumen `editorial_ai_n8n_data`.
- Motivo: permite automatizaciones reproducibles sin acoplar n8n al codigo de
  dominio y evita depender del estado manual de Docker Desktop o comandos sueltos.
- Nota operativa: la web/API de la plataforma debe exponerse en el host con
  puerto `8765`; los workflows la consumen desde Docker mediante
  `host.docker.internal`.
- Migracion futura: PostgreSQL y HTTPS cuando haya ejecuciones 24/7, usuarios,
  colas o despliegue fuera de la maquina local.

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

## ADR-0007: Market Intelligence por proxies KDP

- Estado: aprobada
- Decision: crear una capa `market_intelligence` con top 10 de nichos y
  subnichos por ventanas `1y`, `6m`, `1m` y `15d`.
- Motivo: Amazon KDP no publica vistas/compras globales por nicho; el sistema
  debe trabajar con proxies trazables y dejar claro el nivel de confianza.
- Implementacion actual: proveedor local `local_kdp_market_proxy_v1`, boton
  `Refresh KDP market`, endpoint `/api/market-intelligence/refresh` y snapshots
  persistidos en SQLite.
- Proveedores futuros: Keepa para sales rank historico, DataForSEO Amazon para
  volumen de busqueda, Amazon Product Advertising API para sales rank publico,
  Amazon Ads y KDP Reports propios cuando existan libros publicados.
