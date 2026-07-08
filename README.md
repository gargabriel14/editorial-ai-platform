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
python -m editorial_ai.cli run-demo --db data/editorial_ai.sqlite --out outputs/demo
python -m editorial_ai.cli list-opportunities --db data/editorial_ai.sqlite
```

API opcional con FastAPI:

```powershell
pip install -e ".[api]"
uvicorn editorial_ai.api.app:app --reload
```

## Filosofia de arquitectura

Cada modulo tiene un servicio de dominio reutilizable. El pipeline principal solo
orquesta esos servicios. Las integraciones externas se aislan detras de puertos
y adaptadores para poder cambiar proveedores sin reescribir el negocio.

Documentacion principal:

- [Arquitectura](docs/architecture.md)
- [Automatizaciones](docs/automation_playbook.md)
- [Integraciones API](docs/api_integrations.md)
- [Modelo operativo CEO IA](docs/ai_ceo_operating_model.md)

