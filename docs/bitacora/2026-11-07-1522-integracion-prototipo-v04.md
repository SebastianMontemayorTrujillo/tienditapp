# 2026-11-07 15:22 CDMX · integración · Prototipo FastAPI v0.4

- **PR / commits:** integración [#3](https://github.com/carlosgdelvalle/tienditapp/pull/3), `fd9ac89`; seguimiento documental en la rama `cdv/registro-integracion-v04`.
- **Qué cambió:** incorporada `prototypes/tiendita-inteligente-pey-v0.4/`, con vista de empleado, propuesta de carrito desde texto/dictado, separación de cobros de prueba y consulta autenticada a PEY antes de aplicar la confirmación. El prototipo local se reinició en v0.4, modo DEMO, usando una copia de la base v0.3 migrada a las nuevas columnas.
- **Por qué:** integrar la rama solicitada por Carlos y facilitar sus pruebas locales. Se conserva el alcance de aplicación principal definido en [0001](../decisiones/0001-stack.md); v0.4 es un prototipo independiente.
- **Evidencia:**
  ```text
  pytest -q test_flujos.py test_pey_integracion.py test_v04.py (prototipo v0.4)
  15 passed; PEY y OpenAI simulados

  node --check static/app.js
  node --check static/empleado.js
  Ambos: exit 0

  ./scripts/verificar.sh (entorno con app/requirements.txt)
  Sin hallazgos con los patrones mínimos de secretos; 12 passed; VERIFICAR: OK

  GET http://127.0.0.1:8765/openapi.json -> HTTP 200, version 0.4.0
  GET /api/health -> HTTP 200, mode DEMO
  GET / y /empleado -> HTTP 200
  GET /api/bootstrap y /api/employee/bootstrap -> HTTP 200, 8 productos
  Copia SQLite v0.3 -> v0.4: columnas nuevas presentes y PRAGMA quick_check = ok
  ```
  [CI del commit de integración](https://github.com/carlosgdelvalle/tienditapp/actions/runs/42415261362): aprobada, incluidos secretos con gitleaks y pruebas de la app principal.
- **Riesgos abiertos:** esta validación no acredita PEY/OpenAI en vivo ni el dictado por micrófono o la experiencia visual en un teléfono. El servidor del prototipo está limitado a localhost y modo DEMO.
- **Siguiente:** probar la interfaz de empleado en `/empleado`; evaluar por separado qué mejoras del prototipo se incorporan a `app/`.
