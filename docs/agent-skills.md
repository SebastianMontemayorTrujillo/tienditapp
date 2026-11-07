# Agent Skills de Addy Osmani

Instalación local de Codex verificada el 2026-11-07. Fuente: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills), siguiendo su [guía oficial para Codex](https://github.com/addyosmani/agent-skills/blob/main/docs/codex-setup.md).

## Instalación realizada

```bash
codex plugin marketplace add addyosmani/agent-skills
codex plugin add agent-skills@agent-skills --json
```

- Plugin: `agent-skills@agent-skills`, versión `0.6.15`.
- Commit de origen: [`301b02b12bff98e4688e6984af6556802322bbde`](https://github.com/addyosmani/agent-skills/commit/301b02b12bff98e4688e6984af6556802322bbde).
- `codex plugin list --json` confirmó `installed: true` y `enabled: true`.
- Se comprobaron **25 skills** con `SKILL.md` y **7 referencias compartidas** en el paquete instalado.
- Instalación de usuario, fuera de este repositorio; los colaboradores deben instalarla en sus propios entornos. El commit registra la procedencia de esta instalación, no fija futuras instalaciones desde la rama principal.
- Ya existían copias individuales globales. Se conservaron; la instalación completa añade procedencia del plugin y mantiene las rutas de sus referencias compartidas.

## Uso y proceso

Iniciar una sesión nueva de Codex para que descubra el plugin. Las skills estarán disponibles para las siguientes sesiones; esta entrega ya utilizó sus instrucciones desde archivos locales.

Aplicadas para este trabajo: `using-agent-skills`, `spec-driven-development`, `context-engineering` y, por ampliación expresa del usuario, `planning-and-task-breakdown` para teléfonos/computadoras y QR. Se revisó la guía oficial de OpenAI para el empaquetado y descubrimiento de plugins. No se copian las instrucciones completas de las skills a `AGENTS.md`: se cargan según la tarea.

Paquete de definición preparado:

- [SPEC.md](../SPEC.md): alcance, reglas, validación y decisiones pendientes.
- [CAPABILITY_MAP.md](../CAPABILITY_MAP.md): módulos y dependencias propuestos.
- Cinco specs por módulo, enlazadas desde el mapa.
- [AGENTS.md](../AGENTS.md): contexto persistente, comandos y límites del proyecto.
- [Plan](../tasks/plan.md) y [tareas](../tasks/todo.md): responsive, lector QR, experiencia Alipay y pruebas de CoDi.

El usuario confirmó stack, dispositivos objetivo, QR de pago, CoDi Banxico y referencia Alipay. Se prepararon specs y un plan con tareas; no se creó scaffold ni código del producto. El mapa y las políticas nuevas siguen en revisión. La siguiente fase requiere resolver las decisiones pendientes antes de implementar las partes afectadas.

Al preparar la publicación, `main` ya contenía el MVP FastAPI/SQLite, instrucciones del equipo y la decisión 0001. Se conservaron durante la actualización de esta rama. Las specs distinguen esa implementación del objetivo Next.js solicitado, reservan `web/` para archivos futuros y registran la transición pendiente en D7; no reemplazan el código ni las decisiones del equipo.
