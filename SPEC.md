# Especificación — Tienditapp MVP

**Fecha:** 2026-11-07. **Estado:** borrador para revisión; sin implementación autorizada en esta solicitud. **Confirmado por el usuario:** objetivo Next.js + TypeScript + Supabase + Vercel, conservando la implementación FastAPI existente; uso en teléfonos y computadoras; escaneo de QR de pago; CoDi Banco de México; Alipay como modelo de experiencia. Las políticas técnicas nuevas siguen como propuestas.

**Actualización al preparar esta rama:** `main` incorporó una aplicación FastAPI/SQLite en [app/](app/README.md) y la [decisión 0001](docs/decisiones/0001-stack.md) la mantiene como MVP del hackatón. Se conserva intacta. Next.js es el objetivo solicitado para estas specs, todavía sin implementación; la migración y su relación con la entrega requieren resolver D7. Las referencias a `web/` son rutas futuras, no una segunda app creada.

## Objetivo

Permitir que un empleado de una tiendita capture una venta desde teléfono o computadora, cobre mediante un QR PEY/CoDi y reciba una confirmación verificable. El propietario debe poder relacionar dinero recibido, productos vendidos, inventario y empleado, sin revisar manualmente la aplicación bancaria. La web también debe incorporar un escáner de QR de pago con cámara o imagen y revisión antes de continuar por la ruta bancaria soportada.

El recorrido mínimo es catálogo → carrito confirmado → venta pendiente → QR → pago verificado → actualización única de inventario y caja → consulta del dueño. Texto asistido y dictado facilitan la captura; los botones de catálogo mantienen el recorrido cuando la IA o el micrófono fallan.

El recorrido de escaneo es Escanear QR → revisión de datos comprobables → autorización bancaria compatible → resultado verificable cuando la integración tenga acceso. La [referencia Alipay/CoDi](docs/ux-codi-alipay.md) distingue esta experiencia de la iniciación de transferencias dentro de una entidad financiera. El [plan móvil/escritorio](tasks/plan.md) y sus [tareas](tasks/todo.md) forman parte de esta entrega por ampliación solicitada.

## Fuentes, supuestos y estado actual

- Producto y demo: [README.md](README.md), [propuesta de la mesa](docs/propuesta-4pm.md), [plan de construcción](docs/plan-construccion.md), [plan de entrega](docs/plan-entrega.md) y [boceto](docs/boceto-producto.html).
- El repositorio contiene una aplicación Python/FastAPI/SQLite ejecutable en `app/`, además de documentación y recursos. No hay una aplicación Next.js ejecutable, proyecto Supabase ni despliegue Vercel acreditado por estos archivos.
- Existe un [prototipo FastAPI](prototypes/tiendita-inteligente-pey-v0.3/README.md), separado. Su [auditoría](docs/AUDITORIA_PROTOTIPO_FASTAPI.md) y sus pruebas simuladas no acreditan integración bancaria.
- Supuesto de alcance: un comercio ficticio, 30 productos y tres usuarios preconfigurados (dueño y dos empleados), sin altas públicas de comercios ni cuentas bancarias durante la demo.
- La entrega del domingo 8-nov a las 13:00 y las responsabilidades personales provienen de los documentos del equipo; no se verificaron con las bases oficiales ni se reasignan aquí.
- No se leyó ninguna credencial ni se consultó una cuenta privada. El [HANDOFF](HANDOFF.md) y la bitácora de `main` registran un pago real previo, pruebas y pendientes del MVP FastAPI; son evidencia del equipo, no una nueva comprobación bancaria realizada por esta rama.

## Alcance y prioridades

| Prioridad | Resultado observable |
| --- | --- |
| Esencial | Un empleado autorizado consulta el catálogo y confirma un carrito con cantidades y precios recalculados por el servidor |
| Esencial | Una venta pendiente obtiene un QR PEY y muestra el importe realmente solicitado |
| Esencial | Lector de QR dentro de Tienditapp mediante cámara o imagen, con revisión; resolución de QR externos e iniciación de pago sujetas al contrato D6 |
| Esencial | Captura, cobro, escaneo y consulta utilizables con tacto en teléfonos y teclado/ratón en computadoras |
| Esencial | Un pago auténtico válido se aplica una sola vez; duplicados, fallos y concurrencia no duplican inventario ni caja |
| Esencial | Una desconexión o webhook perdido se recupera consultando al servidor y conciliando con PEY |
| Esencial | El dueño distingue valor vendido, dinero recibido, existencias y ventas por empleado |
| Previsto para demo | OpenAI propone un carrito a partir de texto o audio y el empleado lo corrige/confirma |
| Previsto para demo | Confirmación visual y anuncio del importe recibido en el teléfono; segundo teléfono mediante suscripción autorizada |

Fuera del MVP: fiado, WhatsApp, crédito, proveedores, campañas, visión artificial, código de barras, predicción, hardware, custodia de fondos y confirmación de pagos sin conexión. Tampoco incluye incorporar automáticamente las funciones adicionales del prototipo.

Recortes sugeridos por el plan previo: segundo teléfono → detalle del panel → dictado de audio. Cualquier recorte se registra antes de cambiar la demo prometida. Verificación auténtica del pago y consistencia de datos son obligatorias.

## Stack y estructura

Stack objetivo confirmado por el usuario: Next.js con App Router + TypeScript, Supabase PostgreSQL + Realtime, despliegue Vercel. El MVP existente permanece FastAPI/SQLite conforme a la decisión 0001; esta rama publica documentación y no cambia esa aplicación. Integraciones previstas del objetivo: API de OpenAI y biblioteca oficial `standardwebhooks`. Vitest para pruebas de lógica/integración; Playwright propuesto para recorrido en navegador. Autenticación Supabase Auth propuesta, pendiente de resolver en D1.

No se fijan versiones ficticias: seleccionar versiones compatibles vigentes mediante documentación oficial al crear el proyecto, registrar Node/package manager y confirmar el lockfile. Los identificadores de modelos de transcripción y extracción siguen pendientes.

```text
AGENTS.md                     reglas persistentes
CAPABILITY_MAP.md             índice de módulos y dependencias
SPEC.md / SPEC-*.md           requisitos y contratos propuestos
tasks/plan.md / todo.md       plan y tareas móvil/escritorio/QR
app/                         MVP FastAPI/SQLite existente; conservar
web/app/                     páginas y adaptadores Next.js (por crear)
web/components/              UI compartida objetivo (por crear)
web/lib/{store,payments,cart,qr}/ reglas/adaptadores objetivo (por crear)
web/supabase/migrations/      esquema PostgreSQL objetivo (por crear)
web/supabase/seed.sql         datos ficticios objetivo (por crear)
web/tests/{unit,integration,e2e}/ pruebas objetivo (por crear)
docs/                        antecedentes, boceto y evidencias sanitizadas
assets/branding/             identidad existente
prototypes/                  aplicación independiente de referencia
```

## Comandos

Hoy se pueden inspeccionar los cambios con `git status --short --branch`, `git diff --stat` y `git diff --check`. La aplicación existente se verifica desde la raíz con `./scripts/verificar.sh` y se ejecuta según [app/README.md](app/README.md); los prototipos tienen instrucciones propias.

Contrato de comandos que deberá materializar el futuro scaffold Next.js en `web/`; **todavía no ejecutable**. Los comandos npm de estas specs y tareas se ejecutarán desde `web/`:

| Propósito | Comando desde `web/` | Condición |
| --- | --- | --- |
| Dependencias reproducibles | `npm ci` | `web/package.json` y `web/package-lock.json` creados |
| Desarrollo | `npm run dev` | configuración local privada lista |
| Compilación | `npm run build` | Next.js configurado |
| Estilo | `npm run lint` | script con ESLint y configuración compartida |
| Tipos | `npm run typecheck` | script `tsc --noEmit` |
| Pruebas sin proveedores reales | `npm run test -- --run` | script Vitest; dobles de PEY/OpenAI |
| Integración transaccional | `npm run test:integration` | PostgreSQL aislado, sin credenciales de producción |
| Recorrido web | `npm run test:e2e` | Playwright y app local con proveedores simulados |

No agregar scripts vacíos para aparentar que estos comandos funcionan. Ya existe `.gitignore` para el MVP; conservarlo y ampliar sus exclusiones para Next.js antes de crear archivos privados o compilados. Las claves del MVP siguen la [decisión 0003](docs/decisiones/0003-credenciales-y-pagos.md).

## Estilo de código

TypeScript estricto, identificadores en inglés, exports nombrados, validación explícita y texto visible en español. No hay un patrón TypeScript existente que copiar; este es un ejemplo propuesto, no código ya implementado:

```ts
type PricedLine = { quantity: number; unitPriceCents: number };

export function calculateTotalCents(items: readonly PricedLine[]): number {
  return items.reduce((total, item) => {
    if (!Number.isSafeInteger(item.quantity) || item.quantity <= 0 ||
        !Number.isSafeInteger(item.unitPriceCents) || item.unitPriceCents < 0) {
      throw new Error("Invalid catalog line");
    }
    const nextTotal = total + item.quantity * item.unitPriceCents;
    if (!Number.isSafeInteger(nextTotal)) throw new Error("Amount out of range");
    return nextTotal;
  }, 0);
}
```

Los precios de este ejemplo ya vienen del catálogo del servidor. Nunca usar un precio enviado por navegador o modelo para persistir el total.

## Reglas comunes y contratos

- Ver el [mapa de capacidades](CAPABILITY_MAP.md) para propietarios de contratos. Los cinco módulos son parte de una aplicación, sin nuevos servicios independientes.
- CoDi Banco de México es la infraestructura objetivo; PEY genera los cobros y proporciona evidencia de recepción. La homologación móvil de las guías Banxico v1.0 entra en vigor el 14-dic-2026; la demo de noviembre debe comprobar el banco y versión disponibles, sin asumir adopción universal.
- Alipay aporta el patrón de escanear, revisar y consultar resultado. No se integra una wallet Alipay ni se supone que la API PEY permita debitar cuentas por leer un QR. El pago autorizado dentro de Tienditapp requiere contrato adicional con una entidad habilitada (D6).
- Identidad, catálogo y ventas se limitan al comercio de la sesión. Un selector visual de empleado no acredita identidad ni permisos.
- Montos internos: centavos MXN enteros. En modo demo, `totalCents` conserva el valor del carrito y `chargedCents = 1`; modo configurado solo en servidor. El QR y los anuncios muestran $0.01. La caja registra dinero realmente recibido.
- Una venta no es un QR y un QR no es una transacción. Conservar IDs internos, intentos de cobro, IDs de QR, transacciones PEY y entregas de webhook por separado.
- Confirmación aceptable: webhook firmado y validado, o consulta autenticada del servidor a PEY que confirma una transacción `PAID` vinculada al QR. Ambos caminos convergen en la misma transacción local. Esto resuelve la contradicción del plan anterior entre “solo webhook” y su conciliación de respaldo.
- Validar importe, relación QR/venta, comercio y cuenta configurada. Validar MXN cuando esté disponible en la evidencia; el webhook QR documenta importe en MXN, sin inventar un campo `currency` obligatorio en ese payload.
- Aplicar recibo, venta, inventario y movimiento de caja atómicamente; las claves únicas y bloqueos protegen contra concurrencia entre webhook, consulta y reintentos.
- Un resultado incierto permanece visible. Generar otro QR requiere resolver primero cualquier intento ambiguo; no se presupone idempotencia del proveedor.
- Hora de negocio: `America/Mexico_City` para corte diario, según el plan del equipo; almacenar instantes UTC. No depender de la zona horaria del teléfono.
- No guardar audio ni cuerpos PEY completos por defecto. Registrar IDs de correlación, origen de evidencia, resultado y error sanitizado. No registrar credenciales ni datos bancarios.

## Estrategia de pruebas y definición de terminado

1. **Lógica:** cantidades/precios, centavos, carrito ambiguo, estados, importes de demo y errores de proveedor. Pruebas deterministas sin red externa por defecto.
2. **PostgreSQL real aislado:** restricciones, permisos, entrega repetida, mismo pago con distinto evento, dos procesos concurrentes, rollback y recuperación. Un mock de base no demuestra atomicidad.
3. **HTTP/navegador:** acceso de dueño/empleado, rechazo entre comercios, QR pendiente, pago confirmado desde servidor, reconexión y datos del reporte. E2E con simulación identificada.
4. **OpenAI:** validación de respuestas con dobles; prueba de calidad en conjunto de diez frases del equipo, objetivo previo ≥9 correctas, con ambiguas como casos separados y sin precios inventados. Evaluación real solo al autorizar uso de API.
5. **Móviles y computadoras:** lector por cámara/imagen, QR escaneable, teclado y tacto, micrófono rechazado, audio tras toque, estado visible por texto/icono y recuperación de red. Seguir matriz y anchos del plan; emulación no sustituye Android/iPhone físicos.
6. **Integración bancaria:** una persona del equipo autoriza el pago real de $0.01 a la cuenta previamente comprobada. Registrar evidencia sanitizada que vincule venta, QR, transacción PEY y actualización única. No sustituirla con pruebas del prototipo.

Cada criterio de módulo requiere su evidencia; una casilla planeada no equivale a una prueba pasada. Al implementar, deben pasar tipos, lint, pruebas relevantes y build, sin suprimir comprobaciones. No se inventa porcentaje de cobertura: los escenarios financieros enumerados son obligatorios y la línea base se medirá con la primera suite.

## Límites operativos

- **Siempre:** mantener las invariantes de pago y permisos; recalcular precios; verificar documentación oficial; conservar evidencia y actualizar specs al cambiar requisitos.
- **Resolver antes de la parte afectada, salvo instrucción ya explícita:** decisiones D1–D7; cambio de stack o alcance; migraciones destructivas; operaciones con dinero, despliegue o entrega externa fuera de lo pedido.
- **Nunca:** publicar claves o datos personales, confiar en un botón “pagado”, confirmar sin conexión, reintentar ciegamente un cobro incierto o presentar simulaciones como evidencia bancaria.

## Decisiones pendientes

| ID | Pregunta | Propuesta para revisión | Cuándo resolver |
| --- | --- | --- | --- |
| D1 | ¿Cómo entran dueño y empleados? | Supabase Auth con usuarios de demo precreados, membresías y acceso por comercio; sin registro público | Antes de esquema y sesiones |
| D2 | ¿Qué versiones y modelos se usarán? | Fijar versiones compatibles y modelos disponibles en la cuenta; texto como respaldo de voz | Antes de scaffold e integración IA |
| D3 | ¿Qué hacer si dos ventas pendientes agotan existencias? | Sin reserva inicial; registrar un pago válido y mostrar déficit en inventario, nunca perder su recibo. Reservas si el equipo exige impedir sobreventa | Antes de confirmar inventario |
| D4 | ¿Quién revisa pagos tardíos, extras y cobros inciertos? | Dueño; lista visible de incidencias. Sin reembolsos ni reasignaciones automáticas en MVP | Antes de diseñar estados y panel |
| D5 | ¿Acceso PEY y cuenta habilitada funcionan hoy? | Comprobar acceso y receptor con el responsable, sin exponer la clave | Antes de integración en vivo |
| D6 | ¿Qué contrato resuelve QR CoDi externos y permite continuar/autorizar el pago? | QR propios verificables primero; cámara/imagen dentro de la web. Importación/escaneo en app bancaria como respaldo; deep link o pago dentro de Tienditapp solo con contrato documentado de participante | Antes de prometer QR externos o pago integral dentro de la app |
| D7 | ¿Cómo se entrega el objetivo Next.js frente al MVP FastAPI ya integrado? | Conservar `app/` y la decisión 0001; reservar `web/` para trabajo futuro. Registrar alcance y transición en una nueva decisión, sin mover ni duplicar código durante esta entrega documental | Antes de crear scaffold o migrar implementación |

Los requisitos confirmados no aprueban implícitamente las políticas propuestas ni el mapa de módulos. La siguiente fase será revisar este paquete y resolver decisiones antes de implementar las partes afectadas. Esta entrega termina en specs, `AGENTS.md` y el plan móvil/escritorio/QR solicitado.

## Referencias técnicas verificadas

Consultadas el 2026-11-07: [contrato PEY OpenAPI, versión 2026-10-20](https://docs.pey.mx/openapi.json), [creación de QR](https://docs.pey.mx/docs/api/create-qr/), [firma Standard Webhooks](https://docs.pey.mx/docs/webhooks/introduction/) y [payload de pago QR](https://docs.pey.mx/docs/webhooks/codi/qr/). Reconsultarlas al implementar; esto no verifica credenciales ni operaciones reales.

Fuentes Banxico y Alipay, con fechas y alcance, en [docs/ux-codi-alipay.md](docs/ux-codi-alipay.md). El scanner y la matriz de dispositivos tienen criterios propios; no anunciar estas capacidades como implementadas.
