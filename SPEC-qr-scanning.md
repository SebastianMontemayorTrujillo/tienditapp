# Especificación — qr-scanning

**Estado:** borrador. Requisito del usuario: escanear QR de pago, usar CoDi de Banco de México y tomar Alipay como modelo. **Depende de:** ningún módulo de negocio para leer un símbolo; consume un adaptador de resolución de `payments` cuando se consulta un cobro conocido. Contexto: [SPEC.md](SPEC.md).

## Objetivo

Ofrecer “Escanear QR” dentro de Tienditapp en teléfonos y computadoras. Leer el código, presentar información comprobable y permitir continuar hacia la autorización bancaria compatible. Reconocer una imagen no prueba autenticidad del cobro ni que exista una transferencia pagada.

La referencia es el recorrido de Alipay de escaneo → revisión → autorización → resultado, adaptado a CoDi. No implica integración con Alipay ni crear saldo, monedero o tokens de débito propios. Ver [modelo de experiencia y fuentes](docs/ux-codi-alipay.md).

## Captura e interfaz

- Ruta propuesta `/escanear`; botón visible en inicio y navegación, accesible con toque o teclado.
- Cámara con permiso explícito, preferencia trasera en teléfono y selector de dispositivo cuando exista más de una. Liberar las pistas al salir, cancelar o pasar a segundo plano.
- Alternativa “Cargar imagen QR” para computadoras sin cámara, permisos denegados y QR guardados en el mismo teléfono. Decodificar localmente; no subir fotografías completas al servidor ni guardarlas por defecto.
- Un lector compatible entre navegadores es requisito. No depender exclusivamente de `BarcodeDetector`; evaluar una biblioteca mantenida y fijar versión al implementar. El detector nativo puede ser una mejora opcional.
- Estados: solicitando permiso, cámara activa, sin cámara, permiso denegado, sin QR, múltiples QR, código no compatible, leyendo, revisión, continuar en banco, pendiente de confirmación y error recuperable.
- Detener lecturas repetidas del mismo código para no crear operaciones duplicadas. Escanear nunca llama automáticamente a creación de cobros ni a una transferencia.

## Resolución y seguridad

El lector devuelve bytes/texto sin ejecutarlos. Límites de imagen y payload, validación de formato y reglas de clasificación se fijan antes de implementar. No abrir URLs, `javascript:`, intentos de deep link, HTML ni instrucciones extraídas automáticamente.

Una lectura óptica exitosa se muestra como “QR leído”. Solo datos resueltos con contrato verificable pueden presentarse como beneficiario e importe comprobados. No deducir CLABE, receptor o firma a partir de un JSON inventado. Si hay varios QR o no se identifica un formato soportado, pedir selección o mostrar “QR no compatible”.

Propuesta de frontera: `payments` resuelve un QR emitido por la propia integración usando su asociación persistida y permisos; el escáner consume un resultado normalizado. La interfaz no recibe credenciales PEY ni usa el payload para consultar recursos arbitrarios. Los usuarios no autorizados reciben solo el resumen público mínimo expresamente diseñado, nunca datos internos de inventario, empleados o cuentas.

**Alcance comprobable inicial:** códigos emitidos por la integración PEY de Tienditapp. El soporte de QR CoDi externos requiere documentación técnica/SDK de decodificación y pruebas de interoperabilidad; la API PEY revisada no publica un endpoint universal de lectura ni débito. Registrar esta dependencia en D6. Un QR externo leído puede exportarse/importarse en la app bancaria, sin afirmar que fue verificado por Tienditapp.

## Autorización y resultado

CoDi se usa como infraestructura de Banco de México mediante PEY para los cobros. El pagador revisa y autoriza en una aplicación participante. Un enlace directo al banco solo se ofrecerá si hay un contrato oficial comprobado para ese banco y dispositivo; no inventar esquemas de URL.

Respaldo operativo: conservar la imagen QR original, permitir descargarla con acción del usuario y mostrar cómo importarla en la app bancaria compatible; también se puede escanear desde otro dispositivo. Verificar la alternativa en los bancos elegidos para demo. Regresar a Tienditapp no confirma pago.

Para cobros de esta integración, solo `payments` confirma el resultado mediante evidencia PEY. Para un pago a un tercero que esta cuenta no puede consultar, mostrar “Resultado no verificable desde Tienditapp”, sin modificar ventas/caja como si hubiera sido confirmado. Una autorización completa dentro de Tienditapp requiere una integración adicional con una entidad participante y su contrato técnico; no está demostrada por instalar un lector QR.

## Estructura, comandos y aceptación

Código previsto: `web/app/escanear/page.tsx`, `web/components/qr-scanner.tsx`, `web/lib/qr/` y pruebas en `web/tests/unit/` y `web/tests/e2e/`. TypeScript estricto y límites de `SPEC.md`. Comandos futuros (desde `web/`): `npm run test -- --run`, `npm run test:e2e`, `npm run typecheck`, `npm run lint`.

- **QR-1:** teléfono con cámara y computadora con webcam leen un QR preparado; computadora sin cámara lo lee desde imagen. La ruta existe dentro de Tienditapp, no solo como instrucción para abrir un banco.
- **QR-2:** permiso denegado, cámara ocupada, imagen corrupta y múltiples símbolos tienen recuperación; la cámara se detiene al salir.
- **QR-3:** un QR PEY propio muestra solo los datos autorizados y conserva importe/receptor; escanear no crea un cobro ni marca una venta pagada.
- **QR-4:** código arbitrario, URL maliciosa y QR Alipay/otros sistemas no soportados no se ejecutan ni se presentan como CoDi válido.
- **QR-5:** se puede continuar por el flujo bancario documentado o importar la imagen original; escaneo, apertura del banco y regreso mantienen pago pendiente hasta evidencia auténtica.
- **QR-6:** QR de teléfono → teléfono, pantalla de computadora → teléfono e imagen en computadora se verifican separadamente. La compatibilidad CoDi externa y cualquier pago dentro de Tienditapp solo se anuncian después de resolver D6 y probarlos.

## Fuentes

[CoDi: pagar escaneando o importando](https://www.codi.org.mx/secundarias/pagar.html), [PEY: creación de QR](https://docs.pey.mx/docs/api/create-qr/) y [guía Banxico de comercios/desarrolladores](https://www.banxico.org.mx/sistemas-de-pago/d/%7BA21AA19F-C855-9E64-98A4-832D9A51B2B0%7D.pdf), consultadas 2026-11-07. La última guía distingue funcionalidad de cobro de terceros y funcionalidad de pago de participantes; confirmar el contrato aplicable con el proveedor antes de integrar iniciación de pagos.
