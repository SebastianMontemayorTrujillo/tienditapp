# Tareas — teléfonos, computadoras y QR CoDi

**Estado:** todas pendientes; plan y tareas propuestos para el objetivo Next.js, todavía sin construir. Contexto: [plan.md](plan.md). Archivos enumerados son futuros, máximo cinco por tarea. Si una tarea supera ese tamaño, dividirla antes de ejecutar. No asignar responsables personales a partir de los documentos históricos.

La aplicación FastAPI de `app/` ya existe; lo pendiente aquí es el objetivo Next.js en `web/`. Los comandos npm se ejecutarán desde `web/`, cuando exista. D7 y el scaffold son prerrequisitos de R1; no crear una segunda aplicación sin resolver esa transición.

## R1 — Navegación adaptable

- [ ] Crear inicio con “Escanear QR” y “Cobrar”, navegación táctil/teclado y contenedor responsive.
- Aceptación: acciones visibles en 320 y 1440 px, foco visible y sin desbordamiento horizontal; no solicita permisos al cargar.
- Verificación: prueba enfocada `npm run test -- --run tests/unit/app-shell.test.tsx` y revisión de ambos anchos.
- Depende de: scaffold y estilos base; no pagos reales.
- Archivos: `web/app/layout.tsx`, `web/app/page.tsx`, `web/app/globals.css`, `web/components/app-nav.tsx`, `web/tests/unit/app-shell.test.tsx`. Tamaño: M.

## R2 — Carrito manual en ambos tamaños

- [ ] Crear catálogo y carrito con una columna en teléfono y dos zonas en computadora.
- Aceptación: mismas cantidades/total en ambos tamaños; cantidades editables con tacto y teclado; precios definitivos vienen del servidor al cobrar.
- Verificación: `npm run test -- --run tests/unit/checkout.test.tsx`; comprobar teclado virtual y zoom; APIs simuladas identificadas hasta integrar `store-core`.
- Depende de: R1 y contrato de catálogo/venta de `store-core`.
- Archivos: `web/app/cobrar/page.tsx`, `web/components/product-list.tsx`, `web/components/cart.tsx`, `web/lib/cart-state.ts`, `web/tests/unit/checkout.test.tsx`. Tamaño: M.

## Revisión tras R1–R2

- [ ] Navegación y carrito funcionan sin IA/cámara, en 320 y 1440 px; build, tipos y lint pasan. Registrar si el servidor sigue simulado.

## R3 — Presentar QR y estado de cobro

- [ ] Crear la pantalla QR con estados pendiente, confirmado, vencido, incierto y error.
- Aceptación: monto real y valor del carrito separados; QR íntegro; ninguna acción local marca pagado.
- Verificación: `npm run test -- --run tests/unit/payment-screen.test.tsx`; escaneo externo del QR y errores con fixture identificado.
- Depende de: R2 y contrato `payments`; confirmación real requiere PAY-9.
- Archivos: `web/app/cobro/[id]/page.tsx`, `web/components/payment-qr.tsx`, `web/components/payment-status.tsx`, `web/tests/unit/payment-screen.test.tsx`. Tamaño: M.

## R4 — Leer QR con cámara o imagen

- [ ] Seleccionar y fijar lector compatible; implementar cámara con permisos y carga de imagen local.
- Aceptación: QR-1/QR-2/QR-4; cámara se libera, cancelación funciona y URL maliciosa no se ejecuta.
- Verificación: `npm run test -- --run tests/unit/qr-reader.test.ts`; Android, iPhone y computadora con/sin webcam sobre HTTPS. Registrar API de decoder y cambios del lockfile.
- Depende de: R1 y documentación de la biblioteca elegida; las pruebas de permisos requieren una URL segura.
- Archivos: `web/package.json`, `web/package-lock.json`, `web/components/qr-scanner.tsx`, `web/lib/qr/decode.ts`, `web/tests/unit/qr-reader.test.ts`. Tamaño: M.

## R5 — Revisar un QR y continuar en banco

- [ ] Conectar `/escanear` al lector, resolver QR propios y mostrar revisión/handoff documentado.
- Aceptación: QR-3/QR-5; datos no comprobados se etiquetan; no se inventa endpoint PEY de débito, estado pagado ni deep link bancario.
- Verificación: `npm run test -- --run tests/unit/qr-review.test.tsx`; probar QR válido propio, externo, vencido y no autorizado; probar importación bancaria elegida con permiso para operación real aparte.
- Depende de: R4, `payments` y D6. Si falta contrato de resolución/handoff, registrar bloqueo de esa capacidad; la lectura óptica no la da por terminada.
- Archivos: `web/app/escanear/page.tsx`, `web/components/qr-review.tsx`, `web/lib/payments/resolve-qr.ts`, `web/app/api/qr/resolve/route.ts`, `web/tests/unit/qr-review.test.tsx`. Tamaño: M.

## Revisión tras R3–R5

- [ ] QR de cobro legible, lector interno real y revisión separados del pago; documentar capacidades de proveedor disponibles y pendientes D6. Build, tipos y lint pasan.

## R6 — Dictado compatible y respaldo manual

- [ ] Adaptar grabación a capacidades/formato soportado y conservar edición por texto/catálogo.
- Aceptación: permiso denegado, formato no soportado o API caída permiten completar carrito manual; ninguna grabación queda activa al salir.
- Verificación: `npm run test -- --run tests/unit/voice-capture.test.tsx`; iPhone y Android reales; evaluación de modelo separada según CART-7.
- Depende de: R2, `cart-capture` y D2 para evaluación real.
- Archivos: `web/components/voice-capture.tsx`, `web/lib/cart/record-audio.ts`, `web/components/cart-input.tsx`, `web/tests/unit/voice-capture.test.tsx`. Tamaño: M.

## R7 — Recuperar estado y mostrar actividad

- [ ] Conectar la recuperación tras suspender/reconectar y el panel adaptable con métricas separadas.
- Aceptación: UX-4/UX-5/UX-6; Realtime solo provoca una lectura autorizada, dueño ve dinero real y empleado no abre el reporte.
- Verificación: `npm run test -- --run tests/unit/merchant-status.test.tsx`; apagar conexión, volver a la pestaña y consultar día CDMX con contratos simulados; permisos y atomicidad mediante suites de los módulos proveedores.
- Depende de: R3/R5 y lecturas/Realtime de `store-core` + `payments`; endpoint del reporte de `merchant-experience` disponible.
- Archivos: `web/lib/payment-status.ts`, `web/app/mi-tienda/page.tsx`, `web/components/store-report.tsx`, `web/components/payment-announcement.tsx`, `web/tests/unit/merchant-status.test.tsx`. Tamaño: M.

## Revisión tras R6–R7

- [ ] Cámara/micrófono opcionales, reconexión y métricas correctas en ambos formatos; ningún fixture cuenta como evidencia bancaria. Build, tipos y lint pasan.

## R8 — Matriz automática de navegadores

- [ ] Configurar cinco proyectos Playwright y probar checkout, scanner con imagen preparada y recuperación.
- Aceptación: recorrido manual pasa en Chromium/Firefox/WebKit; móvil emulado pasa en Chromium/WebKit; controles accesibles y sin pérdida de funciones al cambiar ancho.
- Verificación: `npm run test:e2e`; proyectos definidos en `plan.md`; trazas para fallos. Dependencias Playwright ya disponibles por scaffold; si faltan, crear tarea previa para instalación.
- Depende de: R2–R7 con backend de pruebas aislado.
- Archivos: `web/playwright.config.ts`, `web/tests/e2e/checkout.spec.ts`, `web/tests/e2e/qr-scanning.spec.ts`, `web/tests/e2e/recovery.spec.ts`, `web/tests/e2e/fixtures.ts`. Tamaño: M.

## R9 — Ensayo físico e interoperabilidad

- [ ] Completar la matriz real y el ensayo de escaneo, autorización bancaria y confirmación PEY.
- Aceptación: teléfono→teléfono, computadora→teléfono e imagen en computadora registrados; banco/OS/versiones identificados; toda capacidad sin prueba figura pendiente.
- Verificación: recorrido en Android, iPhone y computadora; pago $0.01 solo por persona autorizada; evidencia sanitizada cumple PAY-9/QR-6. No inferir autorización de dinero o despliegue por esta lista de tareas.
- Depende de: R8, D5/D6 y autorización aplicable para prueba en vivo.
- Archivos: `docs/qa-mobile-desktop.md`, `docs/demo-guion.md`. Tamaño: S; los archivos de evidencia no deben contener credenciales ni datos bancarios.

## Revisión final

- [ ] Tareas con evidencia real, matriz sin resultados inventados, decisiones pendientes visibles y specs actualizadas.
- [ ] Recorrido esencial en teléfono y computadora, lector dentro de Tienditapp y pago CoDi por un contrato soportado.
- [ ] Build, tipos, lint y pruebas relevantes pasan; no se redujeron verificaciones para cerrar la lista. Revisión humana antes de publicar cuando la publicación no esté ya autorizada.
