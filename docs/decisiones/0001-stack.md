# 0001 · Usamos Python + FastAPI + SQLite con frontend estático para el MVP

- **Estado:** vigente para el hackatón (reemplaza la propuesta Next.js + Supabase del plan inicial; confirmar con la mesa)
- **Fecha:** 2026-11-07
- **Contexto:** a las 15:00 del sábado había dos arquitecturas en el repo: un plan Next.js + Supabase sin código y un prototipo FastAPI de Ricardo con la integración de pey resuelta. Quedaban unas 22 horas. El demo tiene que correr aunque no haya deploy ni webhook registrado.
- **Decisión:** la app del MVP vive en `app/`: FastAPI + SQLite + HTML/JS estático, mismo stack que `prototypes/tiendita-inteligente-pey-v0.3/`. La confirmación de pago funciona por conciliación con pey (`GET /transaction/codi/qr/{id}`) y también por webhook firmado cuando haya URL pública.
- **Opciones descartadas:** Next.js + Supabase, porque no había código y duplicaba lo que ya resolvía el prototipo. Modificar el prototipo de Ricardo en su lugar, porque trae fiado y otros flujos fuera del alcance (decisión 0002) y es material de referencia.
- **Consecuencias:** corre en una laptop con `uvicorn` y se prueba desde cualquier teléfono en la misma red. SQLite no sirve en hosting serverless: para el webhook en internet hace falta un servidor con disco (Render/Railway) o un túnel HTTPS. El dictado por micrófono necesita HTTPS o localhost.
- **Cómo se verifica:** `python -m pytest -q app/tests` en verde; `uvicorn app.main:app` responde `/api/bootstrap`.
