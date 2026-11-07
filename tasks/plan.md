# Plan — Tienditapp en teléfonos y computadoras

**Estado:** plan propuesto, sin código implementado. Preparado por petición expresa del usuario como ampliación de la entrega de specs. Requisitos: [SPEC.md](../SPEC.md), [experiencia del comerciante](../SPEC-merchant-experience.md), [lector QR](../SPEC-qr-scanning.md) y [modelo Alipay/CoDi](../docs/ux-codi-alipay.md). Tareas: [todo.md](todo.md).

El MVP FastAPI en [app/](../app/README.md) existe y permanece intacto. Este plan describe el objetivo Next.js confirmado por el usuario, con archivos futuros bajo `web/` y comandos npm ejecutados desde esa carpeta. Resolver D7 antes de iniciar el scaffold; publicar este plan no aprueba una migración ni reemplaza la decisión 0001.

## Resultado y decisiones de diseño

Una sola web Next.js, una URL HTTPS y un backend compartido para Android, iPhone, tablets y computadoras. El navegador puede cambiar la disposición, pero conserva identidad, importes y estados de pago del servidor.

Inicio con dos acciones visibles: **Escanear QR** y **Cobrar**. El lector abre cámara o imagen; el cobro presenta un QR PEY. Ambos llegan a revisión y resultado claros, inspirados en Alipay, con autorización bancaria conforme a la integración CoDi disponible.

## Distribución adaptable

| Ancho CSS propuesto | Captura y cobro | Escáner y QR | Panel del dueño |
| --- | --- | --- | --- |
| 320–767 px | Una columna; catálogo/carrito con acción principal accesible; teclado virtual no tapa el total ni el botón | Cámara ocupa el área disponible, cierre visible, opción imagen; QR completo sin recorte | Métricas apiladas y filas con etiquetas; sin scroll horizontal de página |
| 768–1023 px | Dos zonas solo cuando caben sin comprimir controles; una columna en orientación estrecha | Marco de cámara/QR limitado al espacio útil | Rejilla flexible y listas adaptadas |
| ≥1024 px | Catálogo a la izquierda y carrito a la derecha; ambos operables con teclado | Panel central con cámara/imagen y detalle al lado cuando cabe | Métricas en fila y tabla legible con alternativa estrecha |

Los cortes son decisiones de producto propuestas, no detección de sistema operativo. Reutilizar los mismos componentes; no mantener dos aplicaciones. Comprobar 320, 375, 390, 768, 1024 y 1440 px, orientación horizontal, zoom de texto y zoom 200%; probar reflow equivalente a 320 px sin perder acciones. La referencia de [W3C para reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html) explica este último criterio.

## Tacto, teclado y capacidades del dispositivo

- Controles principales propuestos de al menos 44 × 44 px por comodidad táctil; foco visible, etiquetas y activación mediante teclado. Ninguna acción depende solo de hover, arrastre, color o sonido.
- Márgenes para áreas seguras, barras del navegador y teclado virtual. Permitir zoom; el total fijo nunca cubre el último producto ni bloquea los botones del sistema.
- Pedir cámara/micrófono después de una acción. Ofrecer cancelar, reintentar y alternativa manual; no solicitar permisos al abrir la página de inicio.
- HTTPS para probar permisos reales desde celulares; `localhost` en la computadora no equivale al HTTP de una IP de red en el teléfono. [MDN documenta la exigencia de contexto seguro](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia).
- Lector QR con imagen como alternativa en cualquier dispositivo; selector de cámara para webcam y preferencia trasera en móviles. QR desconocidos no abren enlaces automáticamente.
- Dictado con detección de `MediaRecorder` y formatos mediante [`isTypeSupported`](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/isTypeSupported_static); no asumir un mismo contenedor de audio en iPhone y Android. Captura de texto/catálogo siempre disponible.
- Confirmación de pago visual completa y voz opcional tras habilitación. Al suspender la app se puede detener la voz; al volver consultar servidor antes de presentar estado actualizado.
- PWA instalable queda como mejora posterior. Para el MVP, usar navegador sin instalación. No añadir service worker que almacene respuestas autenticadas, estados de pago ni QR vencidos.

## Matriz de compatibilidad propuesta

| Entorno | Recorrido a comprobar | Evidencia requerida |
| --- | --- | --- |
| Android / Chrome estable | Cámara trasera, imagen, dictado, cobro, regreso del banco | Un teléfono físico; registrar SO/app/navegador |
| iPhone / Safari estable | Permisos, formato de audio, QR, galería, teclado y retorno | Un iPhone físico; registrar versión iOS/Safari |
| Windows / Chrome y Edge | Teclado, webcam o imagen, carrito y panel | Navegadores reales con versiones registradas |
| macOS / Safari | Checkout, imagen/webcam, permiso y panel | Safari real; WebKit automatizado es evidencia adicional |
| Firefox de escritorio | Captura manual, imagen/cámara compatible y estados | Prueba automática y comprobación manual de funciones soportadas |
| Tablet / navegador táctil | Rotación y distribución intermedia | Emulación más dispositivo si hay uno disponible |

Usar la versión estable disponible al ejecutar y registrar qué se probó. No prometer versiones antiguas sin verificarlas. Si falta un dispositivo/OS, registrar “pendiente”, no “compatible”.

[Playwright](https://playwright.dev/docs/browsers) cubre Chromium, Firefox y WebKit, con [emulación de dispositivos](https://playwright.dev/docs/emulation). Su WebKit no es Safari instalado. La [documentación de Chrome](https://developer.chrome.com/docs/chromedriver/mobile-emulation) también distingue emulación de hardware físico; cámara, voz, barras del navegador y cambio a la app bancaria requieren pruebas reales.

## Orden y dependencias

```text
R1 shell adaptable → R2 carrito manual → R3 QR/estados
R1 → R4 escáner óptico → R5 revisión/handoff CoDi
R2 → R6 voz compatible
R3 + R5 → R7 reconexión/actividad
R2–R7 → R8 matriz automática → R9 QA físico
```

Empezar cámara/imagen temprano para detectar incompatibilidades antes de invertir en pulido. Los componentes se pueden construir con proveedores simulados explícitos mientras llega el backend; cerrar una tarea visual no acredita integración bancaria.

Prerrequisitos del producto completo: `store-core`, `payments` y `cart-capture` implementados con sus criterios y decisiones D1–D5 resueltas según corresponda. R5 depende además del contrato D6 de resolución/handoff; ningún fixture sustituye una API bancaria inexistente. El [plan histórico del equipo](../docs/plan-construccion.md) se debe ajustar contra las nuevas specs antes de ejecutar sus tareas de backend.

## Verificación y cierre

Los comandos `npm run test -- --run`, `npm run test:e2e`, `npm run build`, `npm run typecheck` y `npm run lint` son futuros, sujetos a scaffold. Playwright tendrá proyectos con nombres `desktop-chromium`, `desktop-firefox`, `desktop-webkit`, `mobile-chromium` y `mobile-webkit`; podrán ejecutarse con `npm run test:e2e -- --project=mobile-webkit` una vez configurados.

Cerrar cada tarea con su prueba enfocada; correr build/tipos/lint en los puntos de revisión. Probar dos anchos con cada nueva pantalla antes de continuar. Registrar resultados por navegador, sin ampliar pruebas repetidamente cuando no cambió el comportamiento.

Terminado funcional: un comercio cobra desde teléfono y computadora, el escáner lee cámara/imagen dentro del producto, el QR CoDi se autoriza por una ruta financiera soportada, y las pantallas recuperan el pago real sin duplicar inventario/caja. Validar aparte escaneo teléfono→teléfono, computadora→teléfono e imagen→lector. Registrar como limitación cualquier QR externo o banco no probado.

## Riesgos y decisiones pendientes

| Riesgo | Resolución propuesta |
| --- | --- |
| Se confunde decodificar QR con iniciar una transferencia | Estados separados y contrato bancario documentado antes de anunciar pago dentro de la app |
| No existe API PEY de resolución de QR externos/debito | Acotar primer soporte a QR propios; QR externo y handoff universal pendientes D6, sin suplantar el flujo bancario |
| Cámara o micrófono no disponibles | Imagen, texto y catálogo manual |
| iPhone suspende cámara, audio o Realtime | Liberar recursos y reconsultar servidor al recuperar foco |
| El mismo carrito se cobra en dos pestañas | Clave de operación servidor y una sola adquisición del intento; tests de concurrencia de `payments` |
| El banco aún no aplica las guías nuevas | Ensayar con banco/versión elegidos; no depender del plazo futuro de diciembre para la demo de noviembre |
| No hay hardware de QA suficiente | Priorizar Android+iPhone y una computadora; publicar la matriz real y pendientes |

Mantener D1–D7 en la [spec principal](../SPEC.md); no duplicar decisiones incompatibles en este plan. No se ha seleccionado aún biblioteca QR ni autenticación definitiva.
