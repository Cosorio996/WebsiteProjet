# MVP de software para gestión de cumplimiento ISA/IEC 62443

## 1) Alcance del MVP
Construir una primera versión usable para:
- Cargar y organizar requisitos por norma, parte y categoría.
- Evaluar cumplimiento por requisito.
- Adjuntar evidencias trazables.
- Gestionar planes de acción.
- Exportar reporte para auditoría.

## 2) Mockup funcional (pantallas)

### Pantalla A — Login
- Campos: correo, contraseña.
- Botón: Ingresar.
- Recuperación de contraseña.

### Pantalla B — Dashboard
- KPI 1: % de cumplimiento global.
- KPI 2: requisitos críticos abiertos.
- KPI 3: evidencias vencidas o incompletas.
- Gráfico por parte de la norma (2-1, 3-2, 4-1, etc.).
- Tabla de “acciones urgentes”.

### Pantalla C — Catálogo de requisitos
- Filtros: norma, parte, dominio, criticidad, estado.
- Búsqueda por texto libre.
- Lista con columnas: código, título, responsable, estado, última actualización.

### Pantalla D — Detalle de requisito
- Información del requisito (código, descripción, objetivo).
- Estado de cumplimiento: No evaluado / En progreso / Cumplido / No aplica.
- Campo de justificación.
- Historial de cambios (quién, cuándo, qué cambió).

### Pantalla E — Evidencias
- Carga de archivos (PDF, DOCX, imágenes).
- Metadatos: tipo de evidencia, fecha, propietario, vigencia.
- Relación evidencia ↔ requisito (N a N).
- Vista previa y descarga.

### Pantalla F — Plan de acción
- Hallazgo asociado al requisito.
- Prioridad (alta/media/baja).
- Responsable, fecha objetivo, estado.
- Seguimiento con comentarios y adjuntos.

### Pantalla G — Reportes
- Reporte ejecutivo: estado global por parte de la norma.
- Reporte detallado: requisito, evaluación, evidencias, brechas.
- Exportación: PDF y CSV.

### Pantalla H — Administración
- Gestión de usuarios y roles (Admin, Responsable, Auditor).
- Configuración de catálogos (partes, estados, tipos de evidencia).

## 3) Backlog técnico inicial (20 tareas)

1. Definir arquitectura y repositorio base (frontend/backend/db).
2. Configurar autenticación JWT y refresh tokens.
3. Implementar control de acceso por roles (RBAC).
4. Diseñar esquema de base de datos inicial (PostgreSQL).
5. Crear migraciones para entidades principales.
6. Implementar API de normas y partes.
7. Implementar API de requisitos (CRUD + filtros + búsqueda).
8. Implementar API de evaluaciones de cumplimiento.
9. Implementar API de evidencias y relación con requisitos.
10. Integrar almacenamiento de archivos (S3/MinIO).
11. Implementar historial/auditoría de cambios (audit_log).
12. Construir pantalla de login y flujo de sesión.
13. Construir dashboard con KPIs y gráficos básicos.
14. Construir listado y filtros de requisitos.
15. Construir detalle de requisito + edición de estado.
16. Construir módulo de evidencias (subida, listado, descarga).
17. Construir módulo de planes de acción.
18. Generar reporte PDF y exportación CSV.
19. Añadir pruebas automáticas básicas (API + UI smoke).
20. Preparar despliegue con Docker Compose y documentación.

## 4) Modelo de datos mínimo
- `users`
- `roles`
- `standards`
- `standard_parts`
- `requirements`
- `assessments`
- `evidences`
- `requirement_evidences`
- `action_plans`
- `audit_logs`

## 5) Criterios de aceptación del MVP
- Un auditor puede revisar estado y evidencias por requisito.
- Un responsable puede actualizar estado y adjuntar evidencia.
- El sistema produce un reporte exportable con trazabilidad básica.
- Existe historial de cambios para evaluaciones y evidencias.

## 6) Plan de implementación sugerido

### Semana 1
- Arquitectura, autenticación, esquema de datos y APIs base.

### Semana 2
- Módulos de requisitos y evaluaciones.

### Semana 3
- Módulo de evidencias y plan de acción.

### Semana 4
- Dashboard, reportes, pruebas, hardening y despliegue.
