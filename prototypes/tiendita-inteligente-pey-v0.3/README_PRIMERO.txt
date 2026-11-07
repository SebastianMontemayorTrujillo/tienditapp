TIENDITA INTELIGENTE — HACKATHON PEY v0.3
========================================
Estado: APP LOCAL CON INTEGRACION PEY IMPLEMENTADA EN CODIGO, NO ACTIVADA NI PROBADA CONTRA PRODUCCION.
En modo DEMO no se generan cargos, no se envian solicitudes bancarias ni se usa dinero real.

EMPEZAR HOY — DEMO SEGURA
1. Descomprime el ZIP en Windows con Python 3.10+.
2. Ejecuta INICIAR_WINDOWS.bat. Instala dependencias y arranca FastAPI.
3. En Chrome abre http://localhost:8765.
4. Prueba INVENTARIO -> PEDIDOS -> RECEPCION -> VENDER -> QR -> SIMULAR PAGO.
5. Prueba FIADOS -> CREAR CLIENTE -> FIAR VENTA -> SOLICITAR ABONO -> QR o CoDi Push (solo simulaciones).
6. Elige Dueño o Empleado para demostrar distintos perfiles. No es una autenticacion real.
7. En el mismo Wi-Fi, puedes ver la app desde http://IP_LOCAL_DE_TU_PC:8765.
   NO abras el puerto 8765 en Internet. No metas datos reales de clientes.

QUE SE CONECTO EN EL CODIGO (NO ACTIVADO)
- API PEY POST /codi/qr: QR CoDi para venta y abono a fiado.
- API PEY POST /codi/pn: solicitud CoDi Push al celular de 10 digitos.
- Receptor POST /webhooks/pey: firmas Standard Webhooks, antiguedad de 5 minutos,
  conciliacion por referencia/ID/importe, procesamiento unico de evento/transaccion.
- Se descuenta inventario solo tras webhook firmado; los fiados se descuentan cuando se
  entrega mercancia, pero no se cuentan como ventas cobradas.
- Con abonos reales, disminuye saldo de fiado solo tras confirmacion PEY firmada.
- GET /p/{token} permite mostrar QR remoto para abono (solo util fuera de Wi-Fi con HTTPS publico).
- GET /transaction/{id} de PEY esta disponible en pey_gateway.py para una futura conciliacion manual.
- Los avisos al dueño y empleado son internos y se refrescan cada 6 segundos; NO SMS ni push externo.

ANTES DE CONECTAR PRODUCCION REAL — NO SE EJECUTO EN ESTA ENTREGA
1. REVOCA la API key compartida en capturas del chat y emite otra exclusivamente para este proyecto.
2. Configura y valida una cuenta CoDi habilitada para recibir dinero en PEY.
   ATENCION: la cuenta bancaria de pruebas que ofrece PEY es de un tercero; fondos enviados NO se devuelven.
3. En el portal PEY configura webhook HTTPS publico que apunte a
   https://TU_DOMINIO_SEGURO/webhooks/pey y copia su secreto whsec_... al servidor.
4. Prepara despliegue backend protegido HTTPS, acceso por empleado, control de roles, permisos,
   tasa de solicitudes, monitorizacion, acceso a base de datos y backups. El demo local NO tiene esto.
5. Configura en el sistema del SERVIDOR, NO en codigo/JavaScript/GitHub:
   PEY_API_KEY                  = llave nueva, nunca la expuesta
   PEY_WEBHOOK_SECRET          = whsec_... del webhook PEY
   TIENDITA_OPERATOR_TOKEN     = token operador fuerte (>=20 caracteres aleatorios)
   TIENDITA_PUBLIC_URL         = https://tu-dominio-real
   PEY_ENABLE_LIVE             = 1
   PEY_CONFIRM_REAL_MONEY      = YES_I_AUTHORIZE
   PEY_BANK_ACCOUNT_ID         = ID opcional de cuenta CoDi PEY activa (NO es CLABE)
6. Nada de lo anterior activa un pago por si solo: se requiere que un operador autorizado
   pulse en la app la creacion de un QR o envio de una notificacion CoDi Push.
7. Comienza con un cobro minimo en una cuenta TUYA, de forma expresa y controlada;
   la API PEY documenta que la produccion es el unico entorno disponible a noviembre 2026.

PROTECCION Y LIMITACIONES
- El sistema queda en DEMO si PEY_ENABLE_LIVE no esta definido.
- Si se solicita modo real sin cumplir todos los controles, aparece BLOQUEADO (no vuelve a demo silente).
- En modo real, todas las rutas /api/ salvo /api/health exigen X-Tiendita-Operator-Key.
  El navegador solicita ese token, distinto de la API key PEY.
- Esto NO reemplaza un sistema de autenticacion/roles. No publicar el demo para clientes reales.
- Las solicitudes reales no se reintentan automaticamente ante timeout: PEY pudo haberlas creado;
  se marcan REVISAR_PEY para conciliacion manual y evitar duplicados bancarios.
- No se permite cancelar una venta PEY mientras puede llegar el pago.
- Si no llega el webhook (por ejemplo al estar la PC desconectada), la venta permanece pendiente.
- No se procesan reembolsos ni devoluciones con PEY. Si hubo pago e inventario insuficiente,
  se requiere conciliacion/manual; la app no garantiza operacion bancaria en produccion.
- Los cobros bancarios necesitan conectividad del servidor y acceso a PEY. Sin luz, la PC
  local requiere fuente de energia; el celular con bateria conserva vista cacheada y carrito.
- En modo real no se usan passwords de clientes, pero los nombres y telefonos pueden ser datos
  personales sujetos a controles. No poner datos reales en la demo sin desplegar seguridad.

VALIDACION
- Para correr todas las pruebas: python -m pip install -r requirements.txt pytest httpx
- Luego: python -m pytest -q
- 10 pruebas: 4 flujos originales y 6 de integracion PEY con cliente completamente simulado.
- No se realizaron cobros reales ni pruebas autenticadas contra api.pey.mx.
- Documentacion oficial: https://docs.pey.mx/
