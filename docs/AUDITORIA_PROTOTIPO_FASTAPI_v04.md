# Auditoría Tiendita Inteligente PEY v0.4 — 7 nov 2026

**Alcance:** Segunda aplicación independiente del equipo, no reemplaza Next.js/Supabase. Versión v0.3 permanece como antecedente; **v0.4 es la versión actual para pruebas**.

## Cambios implementados
- Interfaz móvil en `/empleado` para seleccionar productos, dictar, revisar carrito y solicitar QR, con polling del estado de pago.
- Separa valor comercial `amount_cents` e importe bancario `charged_cents`; el modo `TIENDITA_TEST_ONE_CENT=1` cobra $0.01 para prueba y etiqueta `PAGADA_PRUEBA`, **NO liquidación comercial**.
- En PEY LIVE: verifica firma del webhook y realiza un `GET /transaction/{id}` autenticado que valida estado, moneda, método, tipo, monto e ID antes de cambiar estado.
- Deduplicación de webhook, notificaciones y descuentos de inventario en la misma transacción SQLite.
- PIN de empleado y cookie firmada cuando PEY LIVE está habilitado. Nunca utilizar datos reales en demo sin autenticación.
- Interpretación de pedido por reglas con alias y cantidades; OpenAI Responses API opcional si existe clave segura en el servidor. Precios siempre de la base.

## Evidencia y límites
- **15/15 pruebas automatizadas pasaron**; PEY y OpenAI probados solo con dobles/mocks.
- Chequeo de sintaxis JavaScript completado para interfaces dueño/empleado.
- La automatización de Chrome fue bloqueada por el entorno (`ERR_BLOCKED_BY_ADMINISTRATOR`), por lo que **QA visual móvil NO aprobado**.
- **Ninguna transacción bancaria real verificada**. No se configuró cuenta PEY ni webhook público ni servicio HTTPS. No se realizó envío a teléfonos de clientes.
- Pendientes: recuperación automática si nunca llega webhook, expiración y conciliación integral, autenticación de producción, despliegue HTTPS, dictado/micrófono verificado en teléfono, IA real, pruebas multiteléfono.
- Ninguna credencial PEY/OpenAI ni archivos `.db` o `.env` reales incluidos.

## Rutas
- Admin dueño: `/`
- Empleado: `/empleado`
- PEY webhook: `/webhooks/pey` (no coincide con ruta Next.js prevista en la aplicación principal).
- Instrucciones: `prototypes/tiendita-inteligente-pey-v0.4/README.md`

## Separación
No modifica `app/`, `lib/`, `supabase/` ni la arquitectura definida por Carlos. Revisar antes de fusionar.
