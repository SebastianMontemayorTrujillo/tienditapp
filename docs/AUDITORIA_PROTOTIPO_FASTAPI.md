# Auditoría de incorporación — prototipo independiente Python/FastAPI v0.3

**Origen:** Tiendita Inteligente local desarrollada durante Hackathon PEY.
**Destino:** `prototypes/tiendita-inteligente-pey-v0.3/`.
**Estado:** material de referencia; integración real no verificada.

## Diferencias con la arquitectura del equipo
- El repositorio principal documenta Next.js + TypeScript + Vercel + Supabase y módulos de IA/voz; el prototipo adjunto utiliza Python/FastAPI/SQLite y no integra reconocimiento de voz ni OpenAI.
- La integración de pagos PEY del prototipo fue **probada con respuestas simuladas**. No valida por sí sola un pago bancario real ni la configuración de una cuenta PEY.
- El prototipo expone `/webhooks/pey`; el contrato del equipo establece `/api/webhooks/pey`.
- El contrato principal separa `total_cents` de `charged_cents` para cobros de prueba de 1 centavo. No asumir que los precios semilla del prototipo reflejan ese contrato.
- Roles de dueño y empleado no equivalen todavía a autenticación/autorización de múltiples usuarios.
- Faltan: validación real de webhook, conciliación cuando un webhook no llega, reintentos, expiración/QR ambiguos, operación distribuida y QA en celulares reales.
- Un pago real solo puede confirmarse a partir de datos verificables de PEY, nunca por el botón de simulación.
- El cambio de precios a MX$0.01 que el usuario hizo en su base SQLite local no está incluido.

## Controles de esta propuesta
- Sin archivos existentes de la raíz o de `docs/` modificados, excepto este documento nuevo.
- Sin credenciales reales, `.db`, `.env` privado o CLABE en los cambios propuestos.
- Sin rama principal modificada, sin despliegue ni cobros reales.
- Las 10 pruebas automatizadas se ejecutaron localmente y pasaron (9 advertencias de dependencia); no constituyen QA de integración con PEY real.

## Recomendación de revisión
Carlos y los responsables de pagos/backend deben evaluar por separado qué lógica de inventario, fiados o pruebas se reutiliza. No fusionar este prototipo por considerarlo equivalente al MVP Next.js/Supabase. No debe impedir ni reemplazar el plan del equipo.
