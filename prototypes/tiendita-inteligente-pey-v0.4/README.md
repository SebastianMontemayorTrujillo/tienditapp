# Tiendita Inteligente + PEY v0.4 — prototipo independiente

**Estado:** código actualizado y pruebas automáticas con servicios simulados. **NO está validado contra PEY real, no es seguro para producción y no se ha desplegado.**

Conserva dos vistas de una sola base de datos: **dueño** (`/`) y **empleado** (`/empleado`). No modifica la aplicación principal Next.js/Supabase del equipo Carlos. La rama y PR de GitHub ofrecen código independiente para revisión.

## Cambios desde v0.3

1. **Cobros con comprobación doble:** el servidor comprueba la firma Standard Webhooks sobre el cuerpo original y, antes de registrar la venta, vuelve a consultar `GET /transaction/{id}` usando la credencial PEY del servidor. Exige `PAID`, `MXN`, `CODI`, tipo QR/Push, ID e importe concordantes. Un reintento duplicado no descuenta inventario dos veces. Si no puede hacer la consulta, **no liquida la venta**.
2. **Cobro de prueba separado:** `amount_cents` es el valor del carrito; `charged_cents` es el importe del cobro. `TIENDITA_TEST_ONE_CENT=1` solicita **$0.01 MXN** por venta, aunque el carrito valga más. Un pago bancario verificado en este modo se etiqueta `PAGADA_PRUEBA`, no pago comercial. No se confunde con `DEMO_PAGADA` (simulación sin dinero). El tablero separa ingresos comerciales, cobros de prueba y simulaciones.
3. **App del empleado:** ruta `/empleado`, interfaz móvil para escoger empleado, seleccionar artículos, dictar pedido, confirmar carrito, solicitar QR y ver el estado. En modo PEY REAL requiere PIN y cookie firmada, limitada a operaciones de empleado. La administración del dueño permanece en `/` y utiliza el token del operador. **La seguridad aún requiere evaluación antes de cualquier producción**.
4. **Dictado y carrito sugerido:** Chrome u otro navegador compatible puede convertir voz a texto mediante `SpeechRecognition`/`webkitSpeechRecognition`. El servidor interpreta nombres, alias y cantidades con reglas locales o, si se establece `OPENAI_API_KEY`, con la API Responses de OpenAI. **No inventa precios ni productos.** El empleado revisa la propuesta antes de incorporarla al carrito. No hay llamadas reales a OpenAI en las pruebas.
5. **Bases de datos anteriores:** `create_database` añade columnas de forma no destructiva; los precios modificados en tu equipo a $0.01 no se empaquetan, pues la base SQLite de tu PC no fue transferida.

## Ejecutar en Windows (demo local, sin dinero)

Abre CMD en la carpeta del proyecto y ejecuta:

```cmd
py -m pip install -r requirements.txt
py -m uvicorn app:app --host 127.0.0.1 --port 8765
```

Dueño: `http://127.0.0.1:8765/`  
Empleado: `http://127.0.0.1:8765/empleado`

La web puede funcionar localmente sin API keys. El botón **Simular pago** nunca cobra. El dictado por micrófono depende del navegador y normalmente requiere HTTPS o localhost. Para abrir desde otro celular se necesita una URL segura/accesible y el despliegue correspondiente; **no** exponemos automáticamente el servidor local.

Para simular solicitudes de **$0.01** sin cambiar el precio del catálogo, en CMD, *antes de ejecutar uvicorn*:

```cmd
set TIENDITA_TEST_ONE_CENT=1
```

El importe cobrado y el valor total se muestran por separado en la app. Para desactivarlo, cierra el servidor y utiliza `set TIENDITA_TEST_ONE_CENT=0` antes de volver a iniciarlo.

## Pruebas

```cmd
py -m pip install -r requirements-dev.txt
py -m pytest -q test_flujos.py test_pey_integracion.py test_v04.py
```

Resultado de referencia en entorno controlado (7-nov-2026): **15/15 pruebas**; se usan objetos PEY simulados y no se ejecuta ninguna transferencia bancaria. `node --check static/empleado.js` y `node --check static/app.js` también pasaron. No hay prueba visual real de navegador o dispositivo físico.

## Para habilitar PEY de forma verificable (pendiente, NO realizado)

1. Disponer de un servidor HTTPS público y seguro para el webhook, cuenta de CoDi habilitada y configuración real de la API key **exclusivamente en el servidor**. Jamás subir la key, el secreto del webhook o datos bancarios a GitHub.
2. Registrar en PEY la URL pública `https://<servidor>/webhooks/pey` y guardar el **secreto del webhook**, distinto de la API key.
3. Crear las variables de entorno del archivo `.env.example` con valores **fuera del repositorio**; la app no carga automáticamente `.env`.
4. Antes del cobro, ejecutar una verificación de solo lectura con PEY; comprobar la cuenta receptora. El modo real queda **bloqueado** si falta cualquiera de las protecciones.
5. Autorización y prueba operativa con persona del equipo: crear QR por $0.01, pagar desde banca real, conservar el ID de la transacción, comprobar `GET /transaction/{id}`=`PAID`, firma válida, estado `PAGADA_PRUEBA`, aviso en los dos dispositivos y no duplicación. Este paso **requiere ejecución externa** que todavía no se ha realizado.

No existe aún una reconciliación automática integral en caso de pérdida definitiva del webhook; tampoco autenticación de producción completa, seguridad multitienda, mensajes SMS/push independientes, ni procesamiento fiable de ventas offline. **No afirmar que esos puntos están resueltos.**

## Contratos/API

- `GET /api/health` — modo disponible.
- `POST /api/employee/login` — nombre `Ana | Luis | María`, `pin` requerido en LIVE.
- `GET /api/employee/bootstrap` — catálogo y notificaciones acotados.
- `POST /api/cart/parse` — propuesta desde texto, fuente `REGLAS` u `OPENAI`, desconocidos y precios del catálogo.
- `POST /api/sales` — venta con `amount_cents`, `charged_cents`.
- `POST /api/sales/{id}/qr` — crea QR (simulado o PEY).
- `POST /api/sales/{id}/push` — crea solicitud CoDi Push (simulada o PEY).
- `GET /api/sales/{id}/status` — estado y fuente de verificación.
- `POST /webhooks/pey` — exige webhook firmado y lectura PEY autenticada en LIVE.

**Fuentes técnicas:** [PEY QR](https://docs.pey.mx/docs/api/create-qr/), [PEY transacción](https://docs.pey.mx/docs/api/get-transaction/), [webhooks PEY](https://docs.pey.mx/docs/webhooks/codi/qr/), [OpenAI Responses API](https://platform.openai.com/docs/api-reference/responses).
