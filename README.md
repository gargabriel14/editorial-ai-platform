# Editorial AI Platform

Plataforma modular para operar una editorial digital basada en IA.

El objetivo no es tener scripts sueltos, sino una base de empresa tecnologica:
modulos independientes, contratos claros, almacenamiento comun, automatizaciones
reutilizables y una capa API para conectar n8n, dashboards y agentes.

## Modulos incluidos

- Investigacion de nichos
- Analisis de tendencias
- SEO para Amazon/KDP
- Base de datos de oportunidades
- Generacion de estructuras de libros
- Automatizacion con n8n
- Publicacion
- Marketing
- Analitica

## Inicio rapido

```powershell
$env:PYTHONPATH="src"
python -m editorial_ai.cli --db data/editorial_ai.sqlite run-demo --out outputs/demo
python -m editorial_ai.cli --db data/editorial_ai.sqlite list-opportunities
python -m editorial_ai.cli --db data/editorial_ai.sqlite serve-web --port 8765
```

La web local queda disponible en `http://127.0.0.1:8765`.

API opcional con FastAPI:

```powershell
pip install -e ".[api]"
uvicorn editorial_ai.api.app:app --reload
```

n8n local con Docker:

```powershell
.\scripts\web.ps1 restart
.\scripts\n8n.ps1 start
.\scripts\n8n.ps1 import-workflow
```

n8n queda disponible en `http://localhost:5678`. El dashboard/API local queda
en `http://127.0.0.1:8765` y n8n lo llama desde Docker usando
`http://host.docker.internal:8765`.

## Filosofia de arquitectura

Cada modulo tiene un servicio de dominio reutilizable. El pipeline principal solo
orquesta esos servicios. Las integraciones externas se aislan detras de puertos
y adaptadores para poder cambiar proveedores sin reescribir el negocio.

Documentacion principal:

- [Arquitectura](docs/architecture.md)
- [Automatizaciones](docs/automation_playbook.md)
- [Integraciones API](docs/api_integrations.md)
- [Modelo operativo CEO IA](docs/ai_ceo_operating_model.md)
- [Comunicacion CEO-CTO](docs/ceo_cto_communication.md)
- [Decision log](docs/decision_log.md)
- [KDP Launch & Brand Readiness](docs/kdp_launch_readiness.md)
- [KDP Market Intelligence](docs/market_intelligence.md)
