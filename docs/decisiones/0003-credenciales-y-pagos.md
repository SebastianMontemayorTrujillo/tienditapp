# 0003 · Las credenciales viven solo en variables de entorno y los pagos de prueba los hace una persona

- **Estado:** vigente (aplicada en el código: `.gitignore`, `.env.example`, CI de secretos)
- **Fecha:** 2026-11-07
- **Contexto:** el repo es público. La key de pey puede generar cobros a nombre de una cuenta real. pey no tiene sandbox, así que cada prueba mueve dinero real y no se devuelve. Hay CLABEs pre-autorizadas de personas de pey.
- **Decisión:** las credenciales solo van en `.env` (ignorado por git) y en las variables de entorno del deploy. La CI bloquea el merge si detecta un secreto. Los pagos de prueba son de $0.01 MXN y los hace una persona desde su app bancaria; ningún script ni agente paga. Las CLABEs solo se capturan en el portal de pey, nunca en el repo.
- **Opciones descartadas:** archivo de key en `~/.config/` (funciona en una máquina, pero no es la convención del deploy y se presta a copiarla a mano); keys en el chat del equipo (quedan en historial de terceros).
- **Consecuencias:** cada persona configura su `.env` a partir de `.env.example`. Si una key se filtra se rota de inmediato y se avisa al equipo; borrar el archivo no basta porque git conserva el historial.
- **Cómo se verifica:** `scripts/verificar.sh` y el job `secretos` de la CI (gitleaks) en verde; `git log -p | grep -iE "whsec_|sk-|Bearer "` sin resultados.
