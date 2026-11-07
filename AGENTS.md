# AGENTS.md · Tienditapp

Manual único para cualquier agente (Codex, Claude, ChatGPT) y para las personas del equipo. Si algo aquí choca con otro archivo, gana este, salvo las decisiones vigentes de `docs/decisiones/`, que ganan sobre todo.

## Qué es esto

Tienditapp: cobros CoDi verificados, ventas e inventario para la tiendita de barrio, desde el teléfono. Hackatón DevDay Exchange CDMX, con pey (API de CoDi) y OpenAI. Entrega final: domingo 8-nov-2026, 13:00 CDMX, por correo a hola@aibuilders.lat. Producto completo en [`README.md`](README.md).

## Mapa de ruteo

| Necesitas | Ruta | Regla |
|---|---|---|
| Correr la app y el demo | `app/README.md` | El `.env` nunca se sube |
| Lógica de pagos (la única que marca una venta pagada) | `app/main.py` → `apply_payment` | Cambios aquí requieren prueba nueva en `app/tests/` y aviso al integrador |
| Cliente de pey y firma de webhooks | `app/pey.py` | Base `https://api.pey.mx`; montos en pesos hacia pey, en centavos adentro |
| Dictado → carrito (OpenAI) | `app/parse.py` | El modelo solo elige `productId` del catálogo; los precios salen de la base |
| Esquema y catálogo demo | `app/db.py` | Catálogo ficticio de la Tiendita de la Esquina |
| Pantallas del teléfono | `app/static/` | Español, verbos simples, sin tecnicismos |
| Qué se decidió | `docs/decisiones/` | Solo se agrega. Cambiar una decisión = PR con OK de la mesa |
| Estado del equipo | `HANDOFF.md` | Lo actualiza el integrador en cada hito; es un reclamo, verifícalo contra git |
| Horarios y recortes | `docs/plan-entrega.md` | El pago real y la confirmación verificada no se recortan |
| Propuesta, modelo de negocio, boceto | `docs/` | Cifras sin fuente no van a láminas |
| Láminas del pitch | `presentacion/` | En orden numérico |
| Prototipo de referencia (Ricardo) | `prototypes/tiendita-inteligente-pey-v0.3/` | Referencia; no es la app del MVP |
| Qué pasó en cada PR | `docs/bitacora/` | Una entrada por PR; no se editan |

## Reglas duras

1. **Credenciales solo en `.env`** (ignorado por git) y en variables de entorno del servidor. Nunca en código, capturas, logs ni chats. Si una key se filtra, se rota: borrar el archivo no basta.
2. **Cada pago de prueba es dinero real** (pey no tiene sandbox). Monto: `$0.01 MXN`. Lo hace una persona desde su app bancaria. Ningún script ni agente paga.
3. **Una venta solo pasa a pagada** en `apply_payment`, con un webhook de firma válida o con la conciliación contra `GET /transaction/codi/qr/{id}`. La pantalla del cliente y el QR no prueban nada.
4. **Nunca se muestra un monto distinto del cobrado.** En modo demo la pantalla dice "Modo demo: se cobra $0.01".
5. **Precios del catálogo en la base**, nunca del cliente ni de la IA.
6. **Lo simulado se etiqueta SIMULADO** (las pruebas usan un `FakePey` marcado así).
7. **Cero datos de terceros.**
8. **Nada está "listo" sin evidencia** en el PR.

## Cómo se trabaja

1. Rama por tarea, PR chico contra `main`.
2. `./scripts/verificar.sh` en verde antes del PR (lo mismo corre la CI).
3. Entrada en `docs/bitacora/` en el mismo PR (copia `_plantilla.md`).
4. No edites `HANDOFF.md` salvo que seas el integrador.

## Comandos

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r app/requirements.txt
cp .env.example .env            # y llena PEY_API_KEY
uvicorn app.main:app --host 0.0.0.0 --port 8000
python -m pytest -q app/tests   # o ./scripts/verificar.sh
```

## Proposed target architecture and documentation scope

The current FastAPI workflow above remains applicable to the existing app. The following instructions cover the user-requested draft target and QR/responsive plan; they do not supersede the implementation recorded in decision 0001. Direct user instructions take precedence over repository defaults.

## Start here

- Read [SPEC.md](SPEC.md), [CAPABILITY_MAP.md](CAPABILITY_MAP.md), and the spec for the module being changed. Load other documents only when relevant.
- The user has authorized publishing the specifications, agent instructions, and phone/desktop plan to a GitHub branch. This request does not implement or migrate the application. The user confirmed the Next.js stack and requested payment QR scanning, Banxico CoDi, and an Alipay-inspired experience (2026-11-07). New technical policies remain drafts.
- Read [tasks/plan.md](tasks/plan.md) and [tasks/todo.md](tasks/todo.md) for the requested responsive/QR plan; all implementation tasks remain unchecked.
- Next session: inspect `git status --short --branch`, preserve existing changes, and check the open decisions in `SPEC.md` against the user's current instructions.
- Use the applicable Addy Osmani skills on demand. Installation and verification are recorded in [docs/agent-skills.md](docs/agent-skills.md). Do not paste entire skills into this file.

## Repository and stack

- Product: a responsive web app for Mexican neighborhood shops, usable on phones and computers; in-app payment QR scanning, verified PEY/CoDi collections, sales, inventory, and owner reporting.
- User-confirmed target stack for the draft specs: Next.js + TypeScript, Supabase (PostgreSQL + Realtime), Vercel, and OpenAI. The existing hackathon app remains FastAPI/SQLite under decision 0001. This documentation branch does not replace it or approve a migration; reconcile delivery/migration scope before scaffolding the target. Exact target versions and model IDs are pending.
- The current runnable application is `app/` (FastAPI/SQLite/static UI). There is no Next.js application or Node lockfile. Reserve future Next.js work for `web/` so it cannot overwrite Python source. Never claim that target build or tests pass before they exist.
- `prototypes/tiendita-inteligente-pey-v0.3/` is a separate Python/FastAPI/SQLite reference application. Its simulated payments and tests do not validate the main application or a real PEY payment. Preserve it unless asked to change it.
- `docs/boceto-producto.html` and `assets/branding/` supply the existing visual direction. Product copy and project documents are Spanish; code identifiers are English.
- Use Alipay as a scan/review/result interaction reference, preserving Tienditapp branding. Read [docs/ux-codi-alipay.md](docs/ux-codi-alipay.md); QR decoding, banking authorization, and verified receipt are distinct capabilities. Do not invent PEY debit APIs or bank deep links.
- The new specs describe the proposed implementation contract. Older SQL, types, and task snippets in `docs/plan-construccion.md` are historical planning material; surface conflicts instead of copying them blindly.

## Commands

Available now, from the repository root:

```bash
git status --short --branch
git diff --check
git diff --stat
```

Reference prototype only, from its own directory, with its Python environment installed:

```bash
python3 -m pip install -r requirements.txt
python3 -m uvicorn app:app --host 127.0.0.1 --port 8765
```

Its test environment additionally needs `pytest` and `httpx`; they are not declared in its `requirements.txt`. Do not install or run that app just to validate a documentation change.

Future Next.js scripts, to be created and verified during scaffolding and run from `web/`:

```bash
npm ci
npm run dev
npm run build
npm run lint
npm run typecheck
npm run test -- --run
npm run test:integration
npm run test:e2e
```

These npm commands are a future target contract, not commands that work in the current checkout. Current app checks remain `./scripts/verificar.sh` as described above. Keep scripts, specs, and these instructions aligned when implementation starts.

## Conventions and verification

- TypeScript strict mode; named exports; small functions; server-only modules for PEY, OpenAI, database privileges, and payment transitions.
- Validate untrusted input at server boundaries. Derive the shop and employee from the authenticated session; reload prices from the catalog. A client-supplied employee ID is not authorization.
- Use integer MXN centavos internally. Keep `totalCents` (basket value) separate from `chargedCents` (requested payment) and actual receipts.
- For the future Next.js target, put business rules in `web/lib/`, HTTP adapters in `web/app/api/`, UI in `web/app/` and `web/components/`, SQL migrations in `web/supabase/migrations/`, and tests in `web/tests/`. The Python implementation remains in `app/`; do not move or rewrite it while publishing docs.
- Follow test-driven development for behavior changes. Payment tests must exercise real PostgreSQL transactions and concurrency as well as mocked provider responses.
- Verify mobile and desktop layouts, keyboard and touch, camera/image scanning, denied permissions, and reconnect. Browser emulation does not replace real Android/iPhone camera and bank-app testing. Keep manual/text checkout available when microphone/camera is unavailable.
- Review relevant tests, types, lint, and build before declaring application work complete. Use real mobile browsers for payment UI verification. Report exact commands, outcomes, and limits; distinguish mocked tests from live evidence.
- Documentation-only work needs link, consistency, and whitespace checks; it does not need an unrelated application test run.

## Boundaries

Always:

- Preserve the user's changes and state assumptions. Update the corresponding spec when a requirement changes.
- Verify framework/provider behavior against official documentation before implementing it; pin actual dependency versions in the lockfile. Before a PR, run `./scripts/verificar.sh` for the current Python app and add an immutable entry to `docs/bitacora/`. Preserve existing decisions and leave `HANDOFF.md` to the integrator.
- Authenticate and scope every sale, report, catalog read, and Realtime subscription. Protect cookie-authenticated mutations against cross-site requests.
- Verify Standard Webhooks signatures over the original body, including timestamp verification. Persist event handling and payment effects atomically; deduplicate both delivery IDs and payment transaction IDs.
- Keep late payments, mismatches, and uncertain QR creation visible for reconciliation. Network loss never proves payment.

Resolve with the user when not already specified or authorized:

- A stack replacement, capability/scope change, authentication policy, overselling policy, or incompatible public contract.
- A destructive migration, real-money operation, deployment, external submission, or release beyond the current request.
- Changes that weaken payment verification, tenant isolation, or an established quality gate.

Never:

- Commit secrets, private `.env` files, CLABEs, customer databases, or raw payment payloads containing personal data. Do not read or print the private PEY key to write specs.
- Expose PEY/OpenAI keys, webhook secrets, or Supabase service-role credentials to a browser, public environment variable, log, or screenshot.
- Mark a payment paid based on a QR, client button, browser timer, screenshot, model output, or Realtime message alone.
- Retry ambiguous PEY QR creation automatically, or acknowledge a webhook as successfully applied before its database transaction commits.
- Silence failing checks, skip tests to obtain a pass, fabricate integration evidence, or replace the main app with the prototype implicitly.
- Treat a planned team assignment, delivery email, or deployment step in old documents as an instruction to contact people or publish now.
