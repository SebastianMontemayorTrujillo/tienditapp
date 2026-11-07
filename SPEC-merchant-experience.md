# Especificación — merchant-experience

**Estado:** borrador. **Depende de:** [store-core](SPEC-store-core.md), [payments](SPEC-payments.md), [cart-capture](SPEC-cart-capture.md) y [qr-scanning](SPEC-qr-scanning.md). Reglas comunes: [SPEC.md](SPEC.md).

## Objetivo y pantallas

Permitir operar desde teléfono y computadora con estados de cobro comprensibles. Usar [el boceto del equipo](docs/boceto-producto.html), recursos existentes y [patrón de interacción Alipay adaptado a CoDi](docs/ux-codi-alipay.md). Todos los textos visibles van en español. Distribución, navegación y pruebas en [tasks/plan.md](tasks/plan.md).

| Pantalla prevista | Comportamiento |
| --- | --- |
| Entrada `/` | Accesos visibles “Escanear QR” y “Cobrar”, sesión según D1, identidad/rol y habilitación de voz |
| Escanear `/escanear` | Cámara o imagen, revisión, QR no compatible y continuación bancaria según D6; escanear nunca equivale a pagar |
| Cobrar `/cobrar` | Catálogo, productos rápidos, texto/dictado, propuesta editable, total y confirmación explícita |
| Cobro `/cobro/[id]` | QR, monto solicitado, aviso de demo, espera, expiración, estado incierto o incidencia |
| Pagado, misma venta | Confirmación del servidor, importe recibido y aviso de voz opcional; ningún botón simula un pago real |
| Mi tienda `/mi-tienda` | Solo dueño: ventas, ingresos, desglose por empleado, existencias bajas e incidencias |

## Contratos y recuperación

Consumir las rutas de `payments` y `cart-capture`; no escribir directamente en tablas de pagos. Realtime es un aviso para consultar el estado autorizado, no evidencia bancaria. Recuperar mediante `GET /api/sales/:id` tras `online`, `visibilitychange`, error de suscripción y espera prolongada. Las suscripciones respetan el comercio y los permisos del usuario.

QR derivado de `qrString` o imagen devuelta, con importe visible y contraste suficiente. Nunca transformar un error o timeout en pantalla verde. Mostrar “Por conciliar” para resultado incierto y “El cobro venció” al expirar. Permitir un nuevo intento solo cuando el servidor lo habilita.

Anunciar mediante `speechSynthesis` el monto realmente recibido; si fue un centavo, decir “Recibiste un centavo”. Usar voz `es-MX` cuando esté disponible, habilitar con interacción y permitir silenciar. No garantizar voz offline ni disponibilidad en todos los dispositivos: el soporte depende del navegador. Evitar avisos repetidos de una misma transacción durante la sesión.

El segundo teléfono recibe únicamente eventos autorizados del comercio/ventas a los que tiene acceso. La notificación del propietario no da a un empleado lectura de ventas de otros empleados por defecto.

## Reporte propuesto

`GET /api/reports/today`, solo dueño. Intervalo del día de negocio `America/Mexico_City`, convertido a UTC para consultar. No mezclar estas métricas:

- `salesValueCents`: valor de catálogo de ventas pagadas/aplicadas, por fecha efectiva de pago.
- `receivedCents`: suma de recibos verificados únicos por fecha de recepción/pago, incluidos ingresos tardíos o adicionales pendientes de asignar.
- `unallocatedCents`: parte de los recibos todavía por revisar; mostrarla separada para que caja no oculte dinero real.
- `salesCount`, `byEmployee`, `lowStock` y `topProducts`: desglose del comercio autorizado; atribuir ingreso solo cuando la venta/empleado esté identificado.

Una venta con carrito $58.00 cobrada a $0.01 en demo muestra ambos valores etiquetados. El reporte nunca afirma que se recibieron $58.00. Pagos pendientes/expirados sin recibo no suman caja; incidencias visibles según D4. Esta precisión reemplaza el ambiguo `DayReport.totalCents` del plan previo.

## Estructura, estilo y pruebas

Código previsto: `web/app/`, `web/components/`, `web/app/api/reports/today/route.ts`; pruebas unitarias de agregados, integración de permisos y E2E. Diseño y mensajes basados en el boceto, etiquetas para lectores de pantalla, foco visible y estados que no dependan solo del color o la voz.

Comandos futuros (desde `web/`): `npm run test -- --run`, `npm run test:integration`, `npm run test:e2e`, `npm run build`, `npm run typecheck`, `npm run lint`. Validación física en celulares además del navegador automatizado; no declarar QA móvil por una captura estática.

## Criterios de aceptación

- **UX-1:** catálogo manual permite llegar al QR aun sin OpenAI/micrófono; cliente no puede alterar importe ni identidad del cobro.
- **UX-2:** QR visible y escaneable desde otro teléfono. Importe de carrito y cobro demo aparecen claramente separados.
- **UX-3:** solo estado confirmado por servidor muestra “pagado”; simulación, espera agotada y desconexión no lo hacen.
- **UX-4:** al perder Realtime y volver a la app, se recupera el estado correcto y no se repiten efectos financieros ni avisos de la misma transacción durante la sesión.
- **UX-5:** el dueño ve una venta atribuida al empleado, stock descontado una vez y caja incrementada por el importe real; el empleado no puede abrir el reporte.
- **UX-6:** prueba en el límite de medianoche CDMX asigna ingresos al día correcto; un pago tardío/adicional queda en caja e incidencias sin duplicar ventas.
- **UX-7:** dos teléfonos autorizados muestran el mismo pago y pueden avisar; si voz no está disponible, la confirmación visual sigue siendo completa.
- **UX-8:** navegación y cobro operan en ancho móvil sin desplazamiento horizontal, con etiquetas, foco visible y mensajes que explican cómo recuperarse de los errores.
- **UX-9:** pantallas utilizables de 320 a 1440 px, con flujo completo en computadora por teclado y en teléfono por tacto; no se requiere cámara/micrófono para capturar una venta.
- **UX-10:** inicio permite abrir el lector QR interno; cámara/imagen, revisión y autorización se diferencian siguiendo QR-1–QR-6 y el patrón de Alipay adaptado.

El recorte del segundo teléfono o de detalles del panel debe registrarse como cambio de alcance. D1 y D4 condicionan permisos e incidencias; no se implementa autenticación por un simple selector de empleado.
