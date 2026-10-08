# Project Tracking — MVP ISA/IEC 62443

## 1. Estado actual del proyecto

### Lo que ya existe

| Componente | Ubicación | Estado |
|---|---|---|
| **Plan del MVP** | `MVP_IEC62443_SOFTWARE_PLAN.md` | Completo — 8 pantallas, 20 tareas, modelo de datos |
| **Esquema SQLite** | `app/db.py` | Tablas: requirements, assessments, evidences, action_plans |
| **Flask app** | `db/db1.py` | Rutas: `/dashboard`, `/direcciones`, `/activos`, `/amenazas`, `/riesgos`, `/activos/cargar_csv` |
| **Scripts MySQL** | `db/db.py`, `db/sco.py` | Importan CVEs/CWEs desde CSV a MySQL (con problemas de seguridad) |
| **Esquema SQL** | `db/schema.sql` | Tablas: clientes, activos, amenazas, vulnerabilidades, riesgos |
| **Datos CSV** | `data/` | 4 archivos con CVEs, CPEs y datos de Nozomi |
| **HTML de prueba** | `index.html` | Solo un "Hola Papero" |
| **Git** | `.git/` | 8 commits |

### Lo que falta para que sea funcional

| Categoría | Qué falta |
|---|---|
| **Backend** | API REST para el MVP 62443, autenticación JWT, control de roles (RBAC) |
| **Frontend** | Las 8 pantallas del plan (login, dashboard, catálogo, detalle, evidencias, plan de acción, reportes, admin) |
| **Base de datos** | Migraciones, conexión funcional, datos semilla |
| **Lógica de negocio** | Evaluación de cumplimiento, gestión de evidencias, planes de acción, reportes PDF/CSV |
| **Almacenamiento** | Subida de archivos (S3/MinIO o local) |
| **Auditoría** | Historial de cambios (audit_log) |
| **Pruebas** | Tests de API y smoke tests de UI |
| **Despliegue** | Docker Compose, documentación |
| **Dependencias** | `requirements.txt` o `package.json` |

---

## 2. Opciones para empezar

| Opción | Descripción | Esfuerzo |
|---|---|---|
| **A) Backend con Flask/FastAPI** | Crear API REST en Python que use `app/db.py` como base, añadir autenticación y las rutas del plan | Medio |
| **B) Frontend con React/Vue** | Construir las 8 pantallas del plan conectándose a una API | Alto |
| **C) App full-stack desde cero** | Backend + frontend + DB + auth completo en 4 semanas (como indica el plan) | Alto |
| **D) Mejorar lo existente** | Arreglar los scripts de `db/` (SQL injection, credenciales), conectar `app/db.py` a un servidor mínimo | Bajo |
| **E) Solo prototipo visual** | Mockups estáticos en HTML/CSS de las 8 pantallas sin lógica | Bajo |

---

## 3. Plan de acción sugerido

### Fase 1 — Backend mínimo (Semana 1)
- [ ] Elegir framework (Flask o FastAPI recomendado)
- [ ] Crear `requirements.txt` con dependencias
- [ ] Convertir `app/db.py` en módulo de conexión reutilizable
- [ ] Crear rutas API para requisitos (CRUD + filtros + búsqueda)
- [ ] Crear rutas API para evaluaciones de cumplimiento
- [ ] Crear rutas API para evidencias
- [ ] Crear rutas API para planes de acción
- [ ] Añadir autenticación JWT básica
- [ ] Añadir control de roles (Admin, Responsable, Auditor)

### Fase 2 — Frontend (Semana 2)
- [ ] Elegir framework (React, Vue o HTML/JS vanilla)
- [ ] Crear pantalla de Login
- [ ] Crear Dashboard con KPIs y gráficos
- [ ] Crear listado de requisitos con filtros
- [ ] Crear detalle de requisito + edición de estado
- [ ] Crear módulo de evidencias (subida, listado, descarga)
- [ ] Crear módulo de planes de acción

### Fase 3 — Reportes y auditoría (Semana 3)
- [ ] Generar reporte PDF (estado global por parte de la norma)
- [ ] Exportación CSV
- [ ] Implementar historial de cambios (audit_log)
- [ ] Añadir comentarios y adjuntos a planes de acción

### Fase 4 — Pruebas y despliegue (Semana 4)
- [ ] Pruebas automáticas de API
- [ ] Smoke tests de UI
- [ ] Docker Compose para despliegue local
- [ ] Documentación de uso
- [ ] Hardening básico (validación de entrada, manejo de errores)

---

## 4. Decisiones pendientes

| Decisión | Opciones | Estado |
|---|---|---|
| **Framework backend** | Flask, FastAPI, Express, Django | Pendiente |
| **Framework frontend** | React, Vue, Angular, HTML/JS vanilla | Pendiente |
| **Base de datos** | SQLite (ya existe), PostgreSQL, MySQL | Pendiente |
| **Almacenamiento archivos** | Local, S3, MinIO | Pendiente |
| **Autenticación** | JWT, OAuth2, Session-based | Pendiente |
| **Despliegue** | Docker Compose, Vercel+Railway, VPS | Pendiente |

---

## 5. Notas y observaciones

- Los scripts en `db/` tienen vulnerabilidades de SQL injection por concatenación de strings
- Las credenciales de MySQL están hardcodeadas en `db/db.py` y `db/sco.py` — no deberían estar en el repositorio
- El esquema SQLite en `app/db.py` es un buen punto de partida para el backend
- Los CSV en `data/` pueden usarse como datos semilla para pruebas
- El plan original estima 4 semanas para el MVP completo

### Gestión de riesgos (Parte 2)

- La vista `riesgo` fue modificada para agrupar por CVE (una fila por CVE, CWEs concatenados con `GROUP_CONCAT`)
- La ruta `/activos/cargar_csv` valida las columnas requeridas antes de procesar
- La carga de CSV previene duplicados: si un CVE ya existe, se salta toda la fila
- Las tablas se pueden limpiar con `TRUNCATE` (respetando llaves foráneas) para volver a cargar datos

---

## 6. Registro de cambios

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-09-30 | Creación del documento de seguimiento | — |
| 2026-10-01 | Vista `riesgo` modificada para agrupar por CVE | — |
| 2026-10-01 | Ruta `/activos/cargar_csv` con validación de columnas y prevención de duplicados | — |
| 2026-10-01 | Limpieza de tablas (TRUNCATE) para recarga de datos | — |
