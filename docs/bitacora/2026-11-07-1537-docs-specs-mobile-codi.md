# 2026-11-07 15:37 · docs · Specs y plan móvil/escritorio CoDi

- **Rama:** `docs/tienditapp-specs-mobile-codi`; base integrada de `main`: `57c480a`.
- **Qué cambió:** especificación del objetivo Next.js solicitado, cinco módulos, reglas para agentes, instalación de skills y nueve tareas de experiencia móvil/escritorio con lector QR y referencia Alipay sobre CoDi/PEY.
- **Por qué:** preparar un contrato revisable antes de implementar. Al actualizar la rama apareció el MVP FastAPI del equipo; se conserva su código, branding, HANDOFF y decisiones 0001–0003. Las rutas futuras del objetivo quedan bajo `web/`, con transición pendiente D7 en [SPEC.md](../../SPEC.md).
- **Evidencia:**
  ```text
  source .venv/bin/activate
  ./scripts/verificar.sh
  Secretos: sin hallazgos con patrones mínimos; gitleaks no instalado.
  Pruebas: 12 passed in 0.42s; VERIFICAR: OK.

  git diff --cached --check
  Sin errores.

  Validación local de documentación:
  15 archivos con enlaces locales, whitespace y fences correctos.
  Sin conflictos pendientes ni cambios en aplicación, prototipos o decisiones.
  ```
- **Riesgos abiertos:** las specs y tareas son borradores, no una migración implementada. Quedan D1–D7, resolución de QR externos y contrato de autorización bancaria. Las pruebas de la app usan PEY simulado; esta rama no realiza pagos, despliegues ni nuevas comprobaciones bancarias. El escaneo mínimo de secretos no reemplaza gitleaks.
- **Siguiente:** revisión de la rama y decisiones pendientes; publicar la rama fue autorizado por el usuario. No se fusiona a `main` ni se modifica `HANDOFF.md`.
