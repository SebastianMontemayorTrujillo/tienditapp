# Especificación — store-core

**Estado:** borrador. **Depende de:** ningún módulo. Contexto, comandos, estilo y límites comunes: [SPEC.md](SPEC.md). Índice: [CAPABILITY_MAP.md](CAPABILITY_MAP.md).

## Objetivo y alcance

Proveer identidad del comercio/operador, catálogo y persistencia consistente a los otros módulos. Este módulo no importa PEY ni OpenAI. La autenticación de demo propuesta requiere resolver D1; elegir un nombre en pantalla no sustituye una sesión.

## Datos y contratos proveedores

Modelo lógico propuesto, pendiente de convertir en migraciones:

| Entidad | Campos/reglas esenciales |
| --- | --- |
| `stores`, `memberships` | Comercio, usuario autenticado, rol `owner`/`employee`; unicidad de membresía |
| `products` | Comercio, nombre, alias, precio en centavos, existencias y umbral de reposición |
| `sales`, `sale_items` | Comercio, empleado, total de catálogo y monto solicitado; partidas con cantidad/precio congelados y referencia al producto |
| `payment_attempts` | Venta, clave de operación local, estado, QR PEY único, monto solicitado y expiración; referencia antes de llamar a PEY |
| `payment_receipts` | ID de transacción PEY único, intento/venta vinculados cuando se conocen, monto recibido, fecha, origen verificado y resultado de aplicación |
| `webhook_events` | `webhook-id` único, estado de procesamiento, IDs de correlación y resultado; sin datos bancarios innecesarios |
| `inventory_movements`, `cash_movements` | Movimientos inmutables ligados al recibo/venta; restricciones que impiden aplicar de nuevo el mismo efecto |

Cada referencia entre entidades conserva el comercio; no basta con UUIDs difíciles de adivinar. Dinero no negativo, cantidades positivas y precios válidos se verifican en servidor y mediante restricciones SQL adecuadas. Los límites de importe deben caber en el tipo elegido.

Contratos internos propuestos:

- `requireStoreSession`: devuelve usuario, comercio y rol de una sesión validada; no acepta el comercio enviado por el cliente como autoridad.
- `getCatalog`: devuelve únicamente productos del comercio autorizado.
- `createPendingSale`: recibe IDs de producto y cantidades, recalcula precios, congela partidas y crea venta/intento local. Una misma clave de operación y contenido devuelve la misma venta; reutilizarla con contenido distinto produce conflicto.
- `recordVerifiedPayment`: recibe evidencia normalizada exclusivamente de código servidor del módulo `payments`; bloquea venta/intento, deduplica transacción y aplica los efectos en una sola transacción PostgreSQL.
- Lecturas autorizadas de ventas y agregados para la experiencia del comerciante; ningún navegador modifica directamente pagos o movimientos.

## Consistencia y permisos

La transacción que aplica un pago incluye recibo, transición de venta, movimientos de inventario, movimiento de caja y resultado del evento cuando hay webhook. Si algo falla, revierte todo y se puede reintentar. No insertar un evento como “procesado” en una transacción separada y después intentar aplicar el pago.

Una transacción bancaria solo genera un recibo y un ingreso de caja. Una venta solo genera una salida de inventario por producto. Un pago adicional es otro ingreso real, con incidencia y sin repetir partidas. Pagos tardíos/desconocidos se conservan para revisión; no se borran por no poder cerrar una venta.

No se descuenta stock al crear un QR. D3 define la política de reservas/sobreventa; los tests deben reflejar la decisión antes de habilitar confirmación real.

Propuesta D1: dueño consulta el comercio y reportes; empleado consulta catálogo, crea ventas propias y lee sus cobros. Cualquier lectura ampliada debe ser explícita. Las políticas de acceso y Realtime deben respetar los mismos límites; el rol privilegiado de Supabase queda en servidor.

## Estructura, estilo y comandos

Código previsto: `web/lib/store/`, migraciones en `web/supabase/migrations/`, semilla ficticia en `web/supabase/seed.sql`; pruebas en `web/tests/unit/` y `web/tests/integration/`. Usar las convenciones y ejemplo de TypeScript de `SPEC.md`.

Cuando exista el scaffold: `npm run test -- --run`, `npm run test:integration`, `npm run typecheck` y `npm run lint`. No hay migraciones ni scripts ejecutables del módulo hoy.

## Criterios de aceptación

- **SC-1:** usuario sin sesión no opera; empleado de otro comercio no puede leer/editar una venta, producto o evento Realtime ajeno.
- **SC-2:** alterar nombre, precio o empleado en la solicitud no cambia los datos derivados del servidor; carrito vacío, cantidad fraccional/no positiva, importe fuera de rango o producto ajeno se rechazan.
- **SC-3:** repetir una operación local de creación no duplica venta ni intento; reutilizar su clave con otro carrito devuelve conflicto.
- **SC-4:** webhook y conciliación concurrentes para una transacción dejan un recibo, un movimiento de caja y una sola salida por partida.
- **SC-5:** un fallo inyectado antes del commit no deja efectos parciales; el reintento completa la operación una sola vez.
- **SC-6:** el catálogo semilla contiene 30 productos ficticios; ningún secreto, cuenta bancaria o dato de cliente real entra en la semilla.
- **SC-7:** el estado de inventario tras dos pagos concurrentes cumple la política D3 elegida y ambos recibos reales se conservan.

Verificación de SC-1 y SC-4–SC-7 sobre PostgreSQL aislado real, además de pruebas unitarias; documentar por separado la ausencia de validación con PEY en vivo. Resolver D1 y D3 antes de implementar sus contratos definitivos.
