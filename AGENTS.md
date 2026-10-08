# AGENTS.md

## Project overview

Dual-purpose repo:
1. **MVP ISA/IEC 62443** — compliance management (requirements, assessments, evidences, action plans). Plan: `MVP_IEC62443_SOFTWARE_PLAN.md`. Tracking: `PROJECT_TRACKING.md`.
2. **Cybersecurity risk management** — imports CVEs/CWEs from CSV into MySQL, calculates risk scores per asset.

## Architecture

- `app/db.py` — SQLite schema for the 62443 MVP (requirements, assessments, evidences, action_plans). Not yet wired to any server.
- `db/db1.py` — Flask app (the only runnable server code). Connects to MySQL `nozomi_test_db`. Routes: `/dashboard`, `/direcciones`, `/activos`, `/amenazas`, `/riesgos`, `/activos/cargar_csv`.
- `db/db.py`, `db/sco.py` — MySQL import scripts. Parse CSVs in `data/` and insert into MySQL.
- `db/Risk.sql` — full MySQL schema (creates `nozomi_test_db`, tables: cliente, activo, amenaza, vulnerabilidad, riesgo_datos, activo_riesgo, control_datos, control_riesgo, cve_scores, view `riesgo`).
- `data/` — CSV seed data (CVEs, CPEs, Nozomi exports).

## Running

```bash
# Flask app (requires MySQL running with nozomi_test_db)
python db/db1.py

# Import CSV data into MySQL
python db/db.py
```

## Known issues

- **Hardcoded MySQL credentials** in `db/db1.py`, `db/db.py`, `db/sco.py` (user `carlos`, password `123`). Do not commit real credentials.
- **SQL injection** in `db/db.py` and `db/sco.py` — queries built via string concatenation. Use parameterized queries.
- No `requirements.txt` or `package.json` — dependencies: `flask`, `mysql-connector-python`.
- No tests, no CI, no linter config.

## Conventions

- Language: Spanish (code comments, UI text, plan docs).
- DB naming: MySQL tables use singular Spanish names (`activo`, `amenaza`, `vulnerabilidad`, `riesgo_datos`).
- The `riesgo` view calculates: `activo.prioridad + ROUND(vulnerabilidad.cve_score/2) + amenaza.prioridad`.

## CSV upload (activos)

- Route: `POST /activos/cargar_csv` in `db/db1.py`.
- Required CSV columns: `node_id`, `matching_cpes`, `cve`, `cve_score`, `cwe_id`, `cwe_name`.
- Validates column headers before processing; skips rows where the CVE already exists (prevents duplicates).
- The `riesgo` view groups by CVE (one row per CVE, CWEs concatenated with `GROUP_CONCAT`).
