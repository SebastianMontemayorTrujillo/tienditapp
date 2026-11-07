TIENDITA INTELIGENTE v0.4 — LEE README.md

Windows CMD en esta carpeta:
  py -m pip install -r requirements.txt
  py -m uvicorn app:app --host 127.0.0.1 --port 8765

Dueño:    http://127.0.0.1:8765/
Empleado: http://127.0.0.1:8765/empleado

Sin claves PEY se usa SIMULACIÓN (sin dinero). Para un centavo simulado:
  set TIENDITA_TEST_ONE_CENT=1
[Configura ANTES de iniciar el servidor.]

NO hay pagos bancarios reales verificados todavía; no uses datos reales.
NO se incluyen llaves, secretos ni bases de datos de clientes.
Consulta README.md para pruebas, diferencias y requisitos PEY.
