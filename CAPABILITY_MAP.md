# Mapa de capacidades — Tienditapp

**Estado:** propuesta para revisión, 2026-11-07. El usuario confirmó Next.js + TypeScript + Supabase + Vercel y añadió soporte móvil/escritorio, escaneo de QR, CoDi Banxico y referencia Alipay. Los límites de módulos son propuestos. Este paquete incluye el plan adicional pedido; no autoriza implementación.

Este es el mapa del objetivo Next.js solicitado, con rutas futuras bajo `web/`. La aplicación FastAPI existente en [app/](app/README.md) y la [decisión 0001](docs/decisiones/0001-stack.md) se conservan. D7 en la spec principal debe resolver la transición antes de crear otra aplicación.

| ID estable | Responsabilidad y contrato proveedor | Depende de | Especificación |
| --- | --- | --- | --- |
| `store-core` | Sesión, permisos, catálogo, venta pendiente y persistencia transaccional de pagos, existencias y movimientos | — | [SPEC-store-core.md](SPEC-store-core.md) |
| `payments` | Creación de QR, webhook, conciliación y normalización de evidencia PEY | `store-core` | [SPEC-payments.md](SPEC-payments.md) |
| `cart-capture` | Texto/audio a propuesta de carrito editable usando el catálogo autorizado | `store-core` | [SPEC-cart-capture.md](SPEC-cart-capture.md) |
| `qr-scanning` | Lector óptico local cámara/imagen; consume resolución de cobros cuando está disponible | `payments` para resolución; lector óptico independiente | [SPEC-qr-scanning.md](SPEC-qr-scanning.md) |
| `merchant-experience` | Pantallas móvil/escritorio, avisos, recuperación, revisión de QR y reporte del propietario | `store-core`, `payments`, `cart-capture`, `qr-scanning` | [SPEC-merchant-experience.md](SPEC-merchant-experience.md) |

Orden de dependencias: `store-core` → `payments` y `cart-capture`; `payments` → resolución en `qr-scanning`; todos → `merchant-experience`. La lectura óptica de `qr-scanning` puede validarse antes con fixtures, sin declarar resolución bancaria completa.

El contrato compartido de datos y transacciones pertenece a `store-core`. El adaptador PEY depende de ese contrato; `store-core` no importa el cliente PEY ni llama al proveedor. La experiencia del comerciante consume los contratos HTTP y los datos autorizados, sin modificar directamente estados financieros.

La [SPEC.md](SPEC.md) define alcance, comandos, estructura, estilo, validación y decisiones pendientes comunes. Cada módulo agrega sus interfaces y criterios de aceptación. No se proponen microservicios: son límites dentro de una sola aplicación Next.js.

El usuario pidió además un [plan móvil/escritorio y QR](tasks/plan.md), con [tareas pendientes](tasks/todo.md), preparado como propuesta. El plan completo del backend se revisará después contra estas specs. [docs/plan-construccion.md](docs/plan-construccion.md) se conserva como antecedente, sin dar sus tareas por implementadas ni aprobadas.
