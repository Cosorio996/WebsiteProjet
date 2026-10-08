-- ============================================================
-- Base de datos (schema)
-- ============================================================
DROP DATABASE IF EXISTS nozomi_test_db;

CREATE DATABASE IF NOT EXISTS nozomi_test_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE nozomi_test_db;

-- ============================================================
-- Tabla: Clientes
-- ============================================================
CREATE TABLE IF NOT EXISTS cliente (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre           VARCHAR(120) NOT NULL,
  email            VARCHAR(255) NOT NULL,
  password         VARCHAR(255) NULL,
  direccion        VARCHAR(255) NULL,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_clientes_email (email)
) ENGINE=InnoDB;

-- ============================================================
-- Tabla: Activos
-- ============================================================
CREATE TABLE IF NOT EXISTS activo (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  direccion        VARCHAR(120) NOT NULL,      -- IP/hostname/identificador
  matching_cpes    TEXT NULL,                  -- según tu ERD (no normalizado)
  nodo             VARCHAR(255) NULL,
  firmware_version VARCHAR(50) NULL,             -- versión del firmware (ej: 8.2.1)
  prioridad        DECIMAL(12,2) NOT NULL DEFAULT 1,
  cliente_id       INT UNSIGNED NOT NULL,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY idx_activos_direccion (direccion, nodo),
  CONSTRAINT fk_activo_cliente
    FOREIGN KEY (cliente_id) REFERENCES cliente(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ============================================================
-- Tabla: Amenazas
-- ============================================================
CREATE TABLE IF NOT EXISTS amenaza (
  id               INT UNSIGNED NOT NULL AUTO_INCREMENT,
  codigo_cwe       VARCHAR(40) NOT NULL,
  name             VARCHAR(255) NOT NULL,
  prioridad        DECIMAL(12,2) NOT NULL DEFAULT 1,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_amenazas_cwe_id (codigo_cwe),
  KEY idx_amenazas_name (name)
) ENGINE=InnoDB;

-- ============================================================
-- Tabla: Vulnerabilidades
-- (En tu ERD: Vulnerabilidades tiene FK a Activos y Amenazas)
-- ============================================================
CREATE TABLE IF NOT EXISTS vulnerabilidad (
  id                 INT UNSIGNED NOT NULL AUTO_INCREMENT,
  cve                VARCHAR(25) NOT NULL,     -- ej: CVE-2023-51440
  cve_score          DECIMAL(4,1) NULL,        -- ej: 7.5
  publicado          DATETIME NULL,
  actualizado        DATETIME NULL,
  created_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),

  KEY idx_vuln_cve (cve)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS riesgo_datos (
  id                 INT UNSIGNED NOT NULL AUTO_INCREMENT,
  vulnerabilidad_id  INT UNSIGNED NOT NULL,
  amenaza_id         INT UNSIGNED NOT NULL,
  created_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),

  UNIQUE KEY riesgo_relaciones(vulnerabilidad_id, amenaza_id),

  CONSTRAINT riesgo_vulnerabilidad
    FOREIGN KEY (vulnerabilidad_id) REFERENCES vulnerabilidad(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  CONSTRAINT riesgo_amenaza
    FOREIGN KEY (amenaza_id) REFERENCES amenaza(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS activo_riesgo (
  activo_id  INT UNSIGNED NOT NULL,
  riesgo_id  INT UNSIGNED NOT NULL,

  UNIQUE KEY idx_riesgos (activo_id, riesgo_id),

  CONSTRAINT x1_activo
    FOREIGN KEY (activo_id) REFERENCES activo(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  CONSTRAINT x1_riesgo
    FOREIGN KEY (riesgo_id) REFERENCES riesgo_datos(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS control_datos (
  id                    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  descripcion	  VARCHAR(255) NOT NULL,	
  categoria         VARCHAR(255) NOT NULL,
  naturaleza       VARCHAR(255) NOT NULL,
  prioridad         DECIMAL(12,2) NOT NULL DEFAULT 1,
  created_at       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  
  KEY idx_control_descripcion (descripcion)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS control_riesgo (
  control_id  INT UNSIGNED NOT NULL,
  riesgo_id  INT UNSIGNED NOT NULL,

  UNIQUE KEY idx_riesgos (control_id, riesgo_id),

  CONSTRAINT x2_control
    FOREIGN KEY (control_id) REFERENCES control_datos(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,

  CONSTRAINT x2_riesgo
    FOREIGN KEY (riesgo_id) REFERENCES riesgo_datos(id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
) ENGINE=InnoDB;

USE nozomi_test_db;

CREATE TABLE IF NOT EXISTS cve_scores (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cve_id VARCHAR(32) NOT NULL,
  cve_r10 DECIMAL(5,2) NULL,
  cvss_value FLOAT NULL,
  epss_value FLOAT NULL,
  kev BOOLEAN NOT NULL DEFAULT FALSE,
  dqs FLOAT NULL,
  residual_risk FLOAT NULL,
  source VARCHAR(128) NULL,
  notes TEXT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_cve_scores_cve_id (cve_id),
  KEY idx_cve_scores_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- CREATE VIEW control AS
-- SELECT ...

-- ============================================================
-- Tabla: Riesgos
-- (En tu ERD: Riesgos tiene FK Vulnerabilidad_ID y Amenaza_ID)
-- ============================================================
CREATE VIEW riesgo AS
SELECT
  cliente.email,
  activo.direccion, activo.nodo, vulnerabilidad.cve, amenaza.codigo_cwe, amenaza.name,
  activo.prioridad + ROUND(vulnerabilidad.cve_score/2) + amenaza.prioridad AS riesgo_valor
FROM cliente,activo,vulnerabilidad,amenaza,riesgo_datos,activo_riesgo
WHERE activo.cliente_id = cliente.id AND
      activo_riesgo.activo_id = activo.id AND
      activo_riesgo.riesgo_id = riesgo_datos.id AND
      riesgo_datos.amenaza_id = amenaza.id AND
      riesgo_datos.vulnerabilidad_id = vulnerabilidad.id
ORDER BY cliente.email,activo.direccion, activo.nodo;

INSERT INTO cliente (nombre,email) VALUES ('Tester Testovic', 'tester@example.com');



