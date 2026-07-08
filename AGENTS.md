# AGENTS.md

## Proyecto

Esta repo es la plataforma operativa de una editorial digital basada en IA.
El CEO puede ser ChatGPT y Codex actua como CTO/arquitecto de software.

## Normas de trabajo

- Mantener modulos independientes y reutilizables.
- Documentar decisiones relevantes en `docs/decision_log.md`.
- Si una tarea se repite, proponer una automatizacion n8n.
- Si se integra una API, aislarla detras de un adaptador o puerto.
- Nada irreversible de publicacion debe ejecutarse sin aprobacion humana.

## Verificacion

Ejecutar antes de cerrar cambios de codigo:

```powershell
$env:PYTHONPATH="src"
python -m unittest discover -s tests -v
python -m compileall src tests
```

## Comandos utiles

```powershell
$env:PYTHONPATH="src"
python -m editorial_ai.cli --db data/editorial_ai.sqlite run-demo --out outputs/demo
python -m editorial_ai.cli --db data/editorial_ai.sqlite serve-web --port 8765
```

