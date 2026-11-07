# HANDOFF · Tienditapp · 2026-11-07 15:30 CST

Lo actualiza el integrador en cada hito. Es un reclamo pasado: si no cuadra con git, gana git.

## Objetivo inmediato
Entrega de la propuesta a las 16:00 (`docs/propuesta-4pm.md`) y primer pago real hecho desde la pantalla de la app.

## Estado verificado
- Pago real CoDi de $0.01 `PAID` a las 15:08 (tx `01M6VXE5HTXV66NPJCR1XY7T4A`), conciliado con pey.
- App en `app/`: 12 pruebas en verde; en local crea QR reales de pey y muestra el flujo completo (ver `docs/bitacora/2026-11-07-1530-a-app-mvp.md`).

## NO VERIFICADO
- Pago real desde la pantalla de la app (falta escanear un QR generado por la app).
- OpenAI en vivo (falta `OPENAI_API_KEY`; hoy usa el intérprete local y lo dice).
- Webhook en internet (falta URL HTTPS pública) y la CI en GitHub Actions.

## Decisiones vigentes
`docs/decisiones/0001` (FastAPI), `0002` (alcance), `0003` (credenciales y pagos).

## No repetir
- No crear otra app en Next.js: el stack quedó en FastAPI (0001).
- La key de pey ya pasó por capturas y chats: rotarla al terminar el hackatón.

## Siguiente paso
Correr `uvicorn app.main:app --host 0.0.0.0 --port 8000`, cobrar una venta y que una persona pague $0.01 al QR de la pantalla.
