# Modelo de experiencia — Alipay sobre CoDi/PEY

**Solicitud del usuario, 2026-11-07:** teléfonos y computadoras, lector de QR de pago dentro del producto, infraestructura CoDi de Banco de México y Alipay como modelo. Este documento define la referencia de producto; no acredita interoperabilidad ya implementada.

## Qué tomar del modelo

Alipay+ documenta dos recorridos diferentes: el cliente escanea el QR del comercio (merchant-presented) y el comercio escanea el código del cliente (user-presented). La referencia elegida para este MVP es **el cliente escanea el cobro del comercio**, con revisión clara antes de autorizar. El segundo recorrido no se presume disponible en CoDi. Fuentes: [merchant-presented](https://docs.alipayplus.com/alipayplus/alipayplus/product_intro_mpp/product_mpm_mpp) y [user-presented](https://docs.alipayplus.com/alipayplus/alipayplus/product_intro_mpp/product_upm_mpp).

| Patrón de referencia | Traducción a Tienditapp |
| --- | --- |
| Acceso inmediato al escáner | “Escanear QR” visible en inicio, cámara o imagen |
| Cobro del comercio | “Cobrar”: carrito → monto → QR PEY para presentar al cliente |
| Revisión antes de pagar | Beneficiario, importe y concepto comprobables, sin edición silenciosa de lo incluido en el QR |
| Autorización clara | “Continuar en mi banco” cuando exista ruta documentada; importación/escaneo en banco como respaldo |
| Resultado inequívoco | Pendiente, confirmado o incidencia; confirmación solo desde proveedor |
| Actividad reciente | Historial del comercio y recibos autorizados, con dinero recibido separado de valor del carrito |

La identidad visual sigue siendo Tienditapp/Tiendita de la Esquina. No copiar logotipos, textos ni pantallas de Alipay. No añadir una superapp, monedero, crédito, servicios o promociones ajenos al MVP por usar esta referencia.

## Qué cambió en Banco de México

La [Circular 9/2026, publicada en el DOF](https://dof.gob.mx/nota_detalle_popup.php?codigo=5790862), incorpora guías para homologar la experiencia móvil de transferencias y señala el **14 de diciembre de 2026** como fecha límite de cumplimiento para los participantes indicados. Al 7 de noviembre esa fecha aún es futura; no asumir despliegue uniforme en todos los bancos.

Las [Guías Banxico, versión 1.0](https://www.banxico.org.mx/marco-normativo/normativa-emitida-por-el-banco-de-mexico/circular-14-2017/%7B470203D9-2C3C-1E33-A51E-3AE1DE2DE6FF%7D.pdf), sección VI.C, páginas 35–43, describen lectura/carga de QR CoDi, revisión y autorización. Su control de versiones, página 51, fija entrada en vigor el 14-dic-2026. Esto sustenta el objetivo de compatibilidad de UX; no proporciona por sí solo una API pública nueva para debitar cuentas.

La [guía para comercios y terceros desarrolladores](https://www.banxico.org.mx/sistemas-de-pago/d/%7BA21AA19F-C855-9E64-98A4-832D9A51B2B0%7D.pdf) distingue las aplicaciones de cobro de la funcionalidad de pago de los participantes. Inferencia de diseño: Tienditapp conserva el modelo de comercio que cobra mediante PEY y necesita un contrato adicional si pretende iniciar pagos bancarios dentro de su propia experiencia. Las guías no acreditan que Tienditapp o PEY tengan esa capacidad habilitada para esta cuenta.

## Contrato de interoperabilidad propuesto

1. Generar el payload CoDi a través de [PEY](https://docs.pey.mx/docs/api/create-qr/), sin inventar formato o firma. Renderizar `qrString` íntegro, con margen de lectura, sin alterar el contenido ni sustituirlo por una URL propia que el banco no comprenda.
2. El scanner de Tienditapp lee cámara/imagen. Resolver y verificar son pasos diferentes. La primera compatibilidad comprobable es con QR emitidos por la propia integración; cualquier CoDi externo requiere el contrato de resolución pendiente D6.
3. Conservar montos/cuenta del cobro. Revisión visible seguida de autorización por la ruta bancaria compatible. No pedir NIP, token ni contraseña del banco dentro de Tienditapp.
4. Registrar pago recibido mediante [webhook PEY firmado](https://docs.pey.mx/docs/webhooks/introduction/) o consulta autenticada del servidor. Regresar del banco, leer QR o mostrar “enviado” en otro dispositivo no sustituyen esa evidencia.
5. Probar por banco/app/versión: escaneo de QR en teléfono, QR en computadora, importación desde galería y recuperación al volver del banco. No afirmar compatibilidad con todos los bancos por probar uno.

La [guía oficial de CoDi para pagar](https://www.codi.org.mx/secundarias/pagar.html) documenta escaneo/importación y autorización en la aplicación financiera. Los deep links universales, tokens de pago presentados por el cliente y débito por la API PEY **no se encontraron en los contratos revisados**. Quedan como investigación contractual antes de prometer pago integral dentro de Tienditapp.

## Puertas de aceptación

- El acceso “Escanear QR” abre un lector real dentro de la web; no basta mostrar un QR propio.
- El QR emitido sigue siendo escaneable por una app bancaria CoDi elegida y documentada.
- Se distingue “QR leído”, “Pendiente de pago” y “Pago confirmado”. El último exige evidencia auténtica.
- La demo etiqueta si solo cubre QR propios, cuál banco se probó y si la autorización se completó fuera de Tienditapp.
- No declarar cumplimiento regulatorio, certificación Banxico o soporte de una nueva API sin evidencia del contrato correspondiente.

Fuentes consultadas el 2026-11-07. Revalidar versiones del proveedor y las guías al implementar.
