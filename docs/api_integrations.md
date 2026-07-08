# Integraciones API

## Criterio de integracion

Una API entra en la plataforma si mejora una de estas cosas:

- Velocidad de investigacion.
- Calidad del scoring.
- Reduccion de trabajo operativo.
- Visibilidad financiera o editorial.
- Capacidad de publicar y aprender mas rapido.

## APIs recomendadas

| API | Para que sirve | Modulos |
| --- | --- | --- |
| OpenAI o LLM compatible | Outlines, QA, marketing, resumenes | estructuras, marketing, publicacion |
| Google Trends / DataForSEO | Demanda, keywords, SERP | nichos, tendencias |
| Keepa o proveedor Amazon | Precio, competencia, demanda | oportunidades, SEO |
| Amazon KDP reports | Ventas, royalties, performance | analitica |
| n8n | Orquestacion y aprobaciones | automatizaciones |

## Patron de implementacion

Las APIs no deben vivir dentro del codigo de negocio. Se implementan como
adaptadores en `integrations` y se conectan a servicios mediante puertos.

Ejemplo:

```text
TrendSource -> GoogleTrendsAdapter
OpportunityRepository -> SQLiteOpportunityRepository
AutomationPublisher -> N8NWebhookPublisher
LLMProvider -> OpenAICompatibleProvider
```

## Seguridad

- Las claves viven en variables de entorno.
- Ningun modulo debe imprimir secretos.
- Toda accion irreversible, como publicar, requiere aprobacion humana.
- Las categorias y reglas de KDP deben validarse antes de publicar porque
  pueden cambiar.

