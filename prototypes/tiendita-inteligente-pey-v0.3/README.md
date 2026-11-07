# Tiendita Inteligente PEY v0.3 — Prototipo independiente

Este directorio conserva **una segunda aplicación**, distinta del proyecto principal Tienditapp de Carlos. No reemplaza ni modifica el stack planificado en `docs/plan-construccion.md`.

**Tecnología:** Python / FastAPI / SQLite / interfaz web estática. Contiene inventario, recepción de mercancía, ventas, fiados, QR demostrativos y cliente PEY, con pruebas basadas en respuestas simuladas.

**Estado:** Prototipo de hackatón; **NO APTO PARA PRODUCCIÓN**. No se ha probado una operación bancaria real contra PEY. No existe autenticación robusta por usuario ni aislamiento multi-tienda. Sus rutas, datos SQLite y semántica de demo difieren de los contratos Next.js/Supabase previstos por el equipo.

## Ejecutar localmente
```bash
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8765
```
Abrir http://127.0.0.1:8765.

## Pruebas
```bash
python -m pytest -q test_flujos.py test_pey_integracion.py
```
En el entorno de preparación: 10 pruebas aprobadas, utilizando dobles de prueba, sin transacciones reales.

## Seguridad y límites
- No subir API keys PEY, secretos de webhook, CLABEs, bases de datos de clientes o `.env` real.
- La plantilla `.env.example` solo indica nombres de variables.
- No confundir pago simulado con transacción bancaria real.
- El cambio a precios $0.01 de la base local del fundador **no forma parte de estos archivos**.
- No integrar directamente `app.py` ni `pey_gateway.py` en las rutas Next.js del equipo.
- Requiere revisión de seguridad, permisos, webhooks y conciliación antes de cualquier uso real.

Esta carpeta se incorporó por PR en borrador **para revisión de referencia**, no como sustitución de arquitectura.
