# KDP Market Intelligence

## Objetivo

Detectar los 10 nichos y subnichos KDP con mayor demanda estimada en ventanas
de 1 ano, 6 meses, 1 mes y 15 dias.

## Realidad de datos

Amazon KDP no expone una API publica con vistas y compras globales por nicho.
KDP Reports sirve para los libros propios de la cuenta. Para mercado externo,
el software debe usar proxies:

- Amazon Best Sellers Rank y rankings por categoria.
- Historico de sales rank de proveedores como Keepa.
- Volumen de busqueda Amazon por keywords, por ejemplo DataForSEO.
- Amazon Ads propios si ya tenemos campanas.
- KDP Reports propios cuando existan titulos publicados.

## Implementacion actual

El modulo `market_intelligence` incluye:

- ventanas: `1y`, `6m`, `1m`, `15d`;
- top 10 por ventana;
- vistas estimadas;
- compras estimadas;
- score de busqueda, intencion de compra, momentum, competencia y fit KDP;
- boton `Refresh KDP market` en el dashboard;
- endpoint `POST /api/market-intelligence/refresh`.

La version actual usa un proveedor local deterministico llamado
`local_kdp_market_proxy_v1`. Es util para construir el flujo de producto y n8n,
pero debe sustituirse por proveedores reales antes de tomar decisiones de
inversion fuertes.

## Proveedores recomendados

- Keepa: historico de sales rank y productos Amazon.
- DataForSEO Amazon: volumen de busqueda Amazon y keywords relacionadas.
- Amazon Product Advertising API: busqueda de items y sales rank publico.
- KDP Reports: ventas, royalties y KENP de nuestros libros.

## Comando local

```powershell
$env:PYTHONPATH="src"
python -m editorial_ai.cli --db data/editorial_ai.sqlite refresh-market --limit 10
```

## Endpoint local

```text
POST http://127.0.0.1:8765/api/market-intelligence/refresh
GET  http://127.0.0.1:8765/api/market-intelligence
```

Desde n8n en Docker:

```text
POST http://host.docker.internal:8765/api/market-intelligence/refresh
```

