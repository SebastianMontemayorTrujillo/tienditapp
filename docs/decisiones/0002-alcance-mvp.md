# 0002 · El MVP es un solo recorrido real: venta dictada → cobro pey → confirmación verificada

- **Estado:** vigente para el hackatón (confirmar con la mesa)
- **Fecha:** 2026-11-07
- **Contexto:** la mesa generó muchas ideas (inventario, IA, fiado, cámara, proveedores, crédito, recompensas, semáforo físico). Con 20 horas, intentar varias pone en riesgo lo único que pey pide sí o sí: una integración funcional con una transacción real. El evento pide construir con OpenAI.
- **Decisión:** solo tienditas. El empleado dicta o escribe la venta (OpenAI propone el carrito con el catálogo y el empleado confirma; botones rápidos de respaldo), se cobra con QR de pey, la venta pasa a pagada solo con confirmación de pey, el teléfono avisa en voz alta (también el del dueño) y se actualizan inventario y corte del día. Todo lo demás es roadmap.
- **Opciones descartadas:** captura por cámara y gemelo digital (decisión de Eduardo: agrega complejidad), escaneo de códigos de barras, fiado por WhatsApp, cobro por push, asistente administrativo tipo chat.
- **Consecuencias:** el demo es corto, real y visible en 3 minutos. Orden de recortes si vamos tarde: aviso al dueño, Mi tienda, dictado por voz (queda texto + botones). El pago real y la confirmación verificada no se recortan.
- **Cómo se verifica:** el guion de demo se ejecuta con transacciones `PAID` reales en pey.
