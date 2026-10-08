-- MVP ISA/IEC 62443 - Esquema de datos base

PRAGMA foreign_keys = ON;

-- 1) CLIENTES
CREATE TABLE clientes (
  cliente_id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name         TEXT NOT NULL,
  email        TEXT NOT NULL UNIQUE,
  address      TEXT,
  created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2) ACTIVOS
CREATE TABLE activos (
  activo_id     INTEGER PRIMARY KEY AUTOINCREMENT,
  activo_name   TEXT NOT NULL,
  descripcion   TEXT,
  activo_valor  REAL,
  cliente_id    INTEGER NOT NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX idx_activos_cliente_id ON activos(cliente_id);

-- 3) AMENAZAS (en tu diagrama parece ser "CVE master")
CREATE TABLE amenazas (
  cve_id            TEXT PRIMARY KEY,        -- ej: "CVE-2026-2905"
  cve_name          TEXT,
  cve_create_time   DATETIME,
  cve_update_time   DATETIME,
  cve_valor         REAL
);

-- 4) VULNERABILIDADES (instancia vinculada a un activo)
CREATE TABLE vulnerabilidades (
  cve_id            TEXT PRIMARY KEY,        -- según tu ERD (ver recomendaciones de normalización)
  cve_score         REAL,
  cve_description   TEXT,
  cve_cvss          TEXT,                    -- en tu dibujo parece "cve_cpss"; lo dejé como CVSS
  cve_create_time   DATETIME,
  cve_valor         REAL,
  activo_id         INTEGER NOT NULL,
  created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (activo_id) REFERENCES activos(activo_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE INDEX idx_vuln_activo_id ON vulnerabilidades(activo_id);

-- 5) RIESGOS
CREATE TABLE riesgos (
  riesgo_id           INTEGER PRIMARY KEY AUTOINCREMENT,
  riesgo_valor        REAL NOT NULL,
  activo_id           INTEGER NOT NULL,
  cve_id_vuln         TEXT NOT NULL,
  cve_id_amenaza      TEXT NOT NULL,
  assessed_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (activo_id) REFERENCES activos(activo_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  FOREIGN KEY (cve_id_vuln) REFERENCES vulnerabilidades(cve_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  FOREIGN KEY (cve_id_amenaza) REFERENCES amenazas(cve_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  -- Evita duplicar el mismo riesgo para la misma combinación
  UNIQUE (activo_id, cve_id_vuln, cve_id_amenaza)
);

CREATE INDEX idx_riesgos_activo_id ON riesgos(activo_id);
CREATE INDEX idx_riesgos_cve_vuln ON riesgos(cve_id_vuln);
CREATE INDEX idx_riesgos_cve_amenaza ON riesgos(cve_id_amenaza);