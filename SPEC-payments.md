# Especificación — payments

**Estado:** borrador. **Depende de:** [store-core](SPEC-store-core.md). Contexto y reglas comunes: [SPEC.md](SPEC.md).

## Objetivo

Vincular una venta a un cobro PEY y convertir evidencia auténtica en efectos locales recuperables y únicos. El módulo verifica el proveedor; `store-core` aplica la transacción local.

## Interfaces HTTP propuestas

| Ruta | Contrato |
| --- | --- |
| `POST /api/sales` | Sesión requerida. Entrada: `operationId`, `items: { productId, qty }[]`. Sin precios ni identidad de empleado autoritativos del cliente |
| `GET /api/sales/:id` | Sesión y permiso. Devuelve `saleId`, `totalCents`, `chargedCents`, estado de venta, estado de intento, QR disponible, expiración y posible incidencia |
| `POST /api/webhooks/pey` | Cuerpo original + encabezados Standard Webhooks; autenticación mediante firma, no mediante sesión de navegador |

Creación exitosa: `201` con `saleId`, ambos importes, `qrString`, `qrImage` opcional y `expiresAt`. Un intento ambiguo responde con referencia persistida y estado de conciliación (propuesta `202`), sin QR inventado. Repetición local devuelve la operación existente. Errores de validación/autorización usan `400`/`401`/`403`, recursos inaccesibles `404`, conflicto `409`; incluir `code` y `requestId` sanitizados. Fijar el esquema final al planificar.

## Contrato PEY verificado

Fuentes: [OpenAPI 2026-10-20](https://docs.pey.mx/openapi.json), [QR](https://docs.pey.mx/docs/api/create-qr/), [firma](https://docs.pey.mx/docs/webhooks/introduction/) y [evento QR](https://docs.pey.mx/docs/webhooks/codi/qr/), consultadas 2026-11-07.

- Crear con `POST /codi/qr`, importe en MXN, expiración propuesta `600`, `metadata.saleId` e ID de intento. Cuenta receptora decidida por servidor; si se indica `bankAccountId`, debe estar habilitada. `qrImage` puede faltar: dibujar el QR desde `qrString`.
- El evento `codi.qr.payment_received` contiene `codiQrId`, `transactionId`, `amount` y `datePaid` Unix en segundos. No confundirlos con el ID interno de venta.
- Recuperación: `GET /transaction/codi/qr/{id}` con paginación `nextToken`; confirmar transacción `PAID`, monto y vínculo. Consultar `GET /transaction/{id}` si hace falta verificar datos adicionales.
- No se observó contrato de idempotencia para crear QR. La idempotencia local no vuelve segura la repetición de un POST que pudo completarse en PEY.
- El módulo proveerá a `qr-scanning` un adaptador para resolver QR propios desde su asociación persistida, devolviendo solo datos autorizados. La ruta propuesta `POST /api/qr/resolve` recibe el payload leído, validado y limitado; el resumen público/autorización se fija con D6. No convertir este adaptador en proxy para recursos externos arbitrarios ni asumir que resuelve todos los QR CoDi.
- Infraestructura objetivo: CoDi Banco de México mediante PEY; compatibilidad y límites en [docs/ux-codi-alipay.md](docs/ux-codi-alipay.md). No hay un endpoint de débito por escaneo establecido en el contrato revisado.

## Estados y recuperación propuestos

Venta: `pending`, `paid`, `expired`. El intento conserva estados separados `creating`, `ready`, `uncertain`, `expired`, `failed`; el recibo/evento registra incidencias como `amount_mismatch`, `late_payment`, `unknown_qr` o `extra_payment`. D4 debe ratificar las reglas de revisión.

1. Persistir venta/intento y clave de operación antes de la petición PEY. Solo un proceso adquiere el intento para crear el QR.
2. Al recibir respuesta, vincular el QR único y persistir la expiración. No devolver éxito financiero por haber generado el QR.
3. Verificar firma y timestamp sobre el cuerpo original antes de procesar. Firma inválida: `401`, sin efectos de negocio.
4. Validar tipo, QR, intento, cuenta/comercio y monto. Si existe cuenta explícita, contrastar su ID; si se usa la cuenta vinculada a la API key, comprobar previamente esa configuración. Los eventos no traen necesariamente todos los campos de la consulta de transacción.
5. Aplicar evidencia mediante `store-core`. Responder `200` solo después del commit o al reconocer una operación ya aplicada. Fallo temporal de persistencia: respuesta reintentable, sin marcar entrega como terminada.
6. Un evento auténtico no aplicable queda persistido con incidencia y puede recibir `200`. Un QR todavía no vinculado debe permitir reprocesamiento tras completar la creación; “recibido” no equivale a “aplicado”.
7. Después de 30 segundos pendiente, una consulta activa de estado puede iniciar conciliación en servidor, con exclusión mutua y límite de frecuencia por intento. La misma comprobación ocurre al volver al primer plano o reconectar. No se presupone un worker que funcione cuando nadie consulta.
8. Un timeout de creación mantiene `uncertain`, bloquea otro QR automático y exige conciliación/revisión. No se promete recuperar el ID de un QR perdido solo por consultar pagos: podría no haber recibido ninguno.
9. Al vencer un QR sin pago confirmado, mostrar `expired`. Revisar pagos antes de ofrecer un nuevo intento de la misma venta. Un pago tardío se registra como dinero recibido e incidencia, sin reactivar ni descontar inventario silenciosamente.

La tardanza se determina por la fecha efectiva de pago verificada, no por la llegada del webhook: un pago efectuado antes de expirar puede confirmarse normalmente aunque la notificación llegue después. Solo el pago efectuado fuera del plazo requiere la política de pago tardío. Probar ambas situaciones.

## Estructura, comandos y límites

Implementación prevista: `web/lib/payments/` y las rutas anteriores en `web/app/api/`. Estilo de `SPEC.md`; adaptadores server-only y evidencia normalizada para `store-core`.

Comandos futuros (desde `web/`): `npm run test -- --run`, `npm run test:integration`, `npm run typecheck`, `npm run lint`. Pruebas automáticas usan dobles PEY, PostgreSQL aislado y secretos sintéticos. Ninguna llamada de escritura PEY ni pago real forma parte de esta entrega documental.

## Criterios de aceptación

- **PAY-1:** carrito de 5800 centavos en demo solicita `0.01` MXN y conserva ambos importes; la cuenta no puede cambiarse desde el cliente.
- **PAY-2:** firma inválida, cuerpo alterado, encabezados ausentes y timestamp fuera de tolerancia no actualizan ventas, stock ni caja.
- **PAY-3:** repetir `webhook-id`, cambiar solo el ID de entrega del mismo pago, o conciliar simultáneamente no duplica efectos.
- **PAY-4:** fallo antes del commit permite reentrega exitosa; un webhook que llega antes de guardar el QR puede recuperarse.
- **PAY-5:** QR ajeno/desconocido, importe inesperado y cuenta distinta no cierran la venta; generan incidencia verificable.
- **PAY-6:** timeout tras crear un QR conserva el intento incierto; doble toque y reintento HTTP no disparan un segundo POST PEY.
- **PAY-7:** sin webhook, una transacción `PAID` aparece al recorrer también páginas posteriores y se aplica por el mismo camino transaccional.
- **PAY-8:** transacción `PENDING`, proveedor caído o teléfono sin red no muestran pago confirmado. Un pago tardío/adicional conserva su recibo sin repetir inventario.
- **PAY-9:** para declarar integración real se requiere evidencia sanitizada de un pago humano autorizado, del receptor correcto, y de su efecto único en la aplicación principal.

PAY-3/PAY-4 requieren pruebas concurrentes y rollback con PostgreSQL real. D4 y D5 siguen abiertas; respuestas simuladas no satisfacen PAY-9.
