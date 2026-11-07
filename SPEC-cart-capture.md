# Especificación — cart-capture

**Estado:** borrador. **Depende de:** [store-core](SPEC-store-core.md). Comandos, estilo y límites comunes: [SPEC.md](SPEC.md).

## Objetivo

Convertir texto o dictado en una propuesta editable de productos existentes, sin que la IA decida precios, permisos, cobros ni movimientos. El empleado confirma siempre el resultado antes de crear una venta.

## Interfaz propuesta

`POST /api/cart/parse`, con sesión y límite de uso por operador/comercio. Mantener la entrada del plan previo: `{ type: 'text' | 'audio', data: string }`; audio como base64 con MIME explícito por definir en el contrato final. Validar formato y tamaño antes de llamar a OpenAI; un límite documentado es requisito de implementación.

Salida `ParseResult`: `items: { productId, name, qty, unitPriceCents }[]`, `unmatched: string[]`. Nombres y precios se recargan del catálogo del servidor. La venta vuelve a validar esos productos y precios al cobrar; esta propuesta no fija precios futuros.

Audio → transcripción → mismo procesamiento que texto. El modelo devuelve IDs y cantidades bajo un esquema validado. IDs fuera del catálogo, cantidades no enteras/no positivas y salida inválida se rechazan. Una frase ambigua queda en `unmatched` para que el empleado elija presentación/tamaño, sin escoger silenciosamente un producto.

No exponer la API key ni enviar datos de otro comercio. Dictados y respuestas del modelo son datos no confiables: no habilitan herramientas de pago, consultas libres a la base ni cambio de instrucciones del sistema. No conservar audio por defecto ni incluirlo en logs.

Si la API falla, el navegador conserva el carrito y permite catálogo/manual. Modelos, topes de audio/texto, timeout y presupuesto necesitan fijarse antes de implementar (D2); no afirmar que un modelo concreto está disponible.

## Estructura y verificación

Implementación prevista: `web/lib/cart/`, `web/app/api/cart/parse/route.ts`; pruebas en `web/tests/unit/` y una evaluación explícita de proveedor separada. TypeScript estricto y convenciones de `SPEC.md`.

Comandos futuros (desde `web/`): `npm run test -- --run`, `npm run typecheck`, `npm run lint`. La suite por defecto no necesita una API key ni consume red. Las evaluaciones reales se ejecutan aparte y registran modelo, versión del catálogo y resultados sanitizados.

## Criterios de aceptación

- **CART-1:** “dos cocas y unas sabritas” produce las cantidades esperadas únicamente si los alias identifican una presentación única; si hay dos tamaños, exige resolver la ambigüedad.
- **CART-2:** producto inexistente va a `unmatched`; ningún precio o ID inventado llega al carrito confirmado.
- **CART-3:** precios enviados por el modelo se descartan; el servidor devuelve los del catálogo autorizado.
- **CART-4:** salida malformada, cantidad fraccional/negativa, prompt malicioso y producto ajeno no crean ventas ni ejecutan cobros.
- **CART-5:** audio transcrito y texto equivalente usan las mismas reglas. Micrófono denegado, audio no soportado o proveedor caído dejan disponible captura manual.
- **CART-6:** el empleado puede ajustar cantidades, resolver `unmatched` y confirmar; interpretar un dictado nunca confirma el carrito automáticamente.
- **CART-7:** conjunto de diez frases no ambiguas del equipo alcanza ≥9 propuestas correctas en evaluación real; las ambiguas se evalúan aparte por rechazo correcto. Registrar cada caso, sin presentar dobles de prueba como evaluación de OpenAI.

Los límites de entrada y gasto son parte del contrato pendiente D2, no un permiso para entrada ilimitada.
