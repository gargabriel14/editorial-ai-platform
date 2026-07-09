# n8n local

Esta carpeta define la instancia local de n8n para la plataforma Editorial AI.

## Requisitos

- Docker Desktop iniciado.
- Web/API de la plataforma disponible en el host cuando se importe el workflow:

```powershell
.\scripts\web.ps1 restart
```

El workflow incluido usa:

- `http://host.docker.internal:8765/api/run-demo`
- `http://host.docker.internal:8765/api/market-intelligence/refresh`

para llamar a la plataforma desde dentro del contenedor.

## Comandos

Desde la raiz de la repo:

```powershell
.\scripts\n8n.ps1 start
.\scripts\n8n.ps1 status
.\scripts\n8n.ps1 logs
.\scripts\n8n.ps1 import-workflow
.\scripts\n8n.ps1 stop
```

n8n queda disponible en `http://localhost:5678`.

El archivo `infra/n8n/.env` se genera localmente y no debe subirse al repositorio.
Contiene `N8N_ENCRYPTION_KEY`, que debe conservarse para poder descifrar las
credenciales guardadas en n8n.
