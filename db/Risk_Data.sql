
-- =============
-- Ejemplo datos
-- =============

INSERT INTO activo (direccion,nodo,prioridad,cliente_id) VALUES (
  'd4:f5:27:94:53:93', 'Servidor Siemens de DA', 5.0,
  (SELECT id FROM cliente WHERE email='tester@example.com')
);
INSERT INTO activo (direccion,nodo,prioridad,cliente_id) VALUES (
  'd4:f5:27:b5:cd:67', 'Servidor S de telecontrol básico', 4.0,
  (SELECT id FROM cliente WHERE email='tester@example.com')
);
INSERT INTO activo (direccion,nodo,prioridad,cliente_id) VALUES (
  '192.168.12.2', 'cpe:/h:siemens:s7-410:-:-:-', 3.0,
  (SELECT id FROM cliente WHERE email='tester@example.com')
);
INSERT INTO activo (direccion,nodo,prioridad,cliente_id) VALUES (
  'd4:45:27:94:53:93', 'cpe:/o:siemens:scalance_firmware:04.02.00:-:-', 2.0,
  (SELECT id FROM cliente WHERE email='tester@example.com')
);
INSERT INTO activo (direccion,nodo,prioridad,cliente_id) VALUES (
  '30:2f:1e:21:4d:3c', 'cpe:/h:siemens:6gk56462gs002ac2:*:*', 5.0,
  (SELECT id FROM cliente WHERE email='tester@example.com')
);

INSERT INTO vulnerabilidad (cve, cve_score) VALUES (
  'CVE-2025-13254', 8.3
);
INSERT INTO vulnerabilidad (cve, cve_score) VALUES (
  'CVE-2023-44373', 9.4
);
INSERT INTO vulnerabilidad (cve, cve_score) VALUES (
  'CVE-2023-44317', 7.2
);

INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'T1','Falsificación de credenciales/omisión de autenticación', 5.0
);
INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-400','Uncontrolled Resource Consumption', 2.0
);
INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-770','Allocation of Resources Without Limits or Throttling', 3.0
);
INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-862','Missing Authorization', 5.0
);
INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-415','Double Free', 4.0
);
INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-476','NULL Pointer Dereference', 4.0
);
INSERT INTO amenaza (codigo_cwe, name) VALUES (
  'CWE-349','Acceptance of Extraneous Untrusted Data With Trusted Data'
);

INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (
  (SELECT id FROM vulnerabilidad WHERE cve='CVE-2023-44317'),
  (SELECT id FROM amenaza WHERE codigo_cwe='CWE-349')
);

INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
  (SELECT id FROM activo WHERE direccion='d4:f5:27:94:53:93'),
  (SELECT riesgo_datos.id
    FROM vulnerabilidad,amenaza,riesgo_datos
    WHERE vulnerabilidad.cve='CVE-2023-44317' AND
          amenaza.codigo_cwe='CWE-349' AND
          riesgo_datos.vulnerabilidad_id=vulnerabilidad.id AND
          riesgo_datos.amenaza_id=amenaza.id
  )
);

INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (
  (SELECT id FROM vulnerabilidad WHERE cve='CVE-2025-13254'),
  (SELECT id FROM amenaza WHERE codigo_cwe='T1')
);

INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
  (SELECT id FROM activo WHERE direccion='d4:f5:27:94:53:93'),
  (SELECT riesgo_datos.id
    FROM vulnerabilidad,amenaza,riesgo_datos
    WHERE vulnerabilidad.cve='CVE-2025-13254' AND
          amenaza.codigo_cwe='T1' AND
          riesgo_datos.vulnerabilidad_id=vulnerabilidad.id AND
          riesgo_datos.amenaza_id=amenaza.id
  )
);

INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'CWE-940','Improper Verification of Source of a Communication Channel', 3.0
);

INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (
  (SELECT id FROM vulnerabilidad WHERE cve='CVE-2025-13254'),
  (SELECT id FROM amenaza WHERE codigo_cwe='CWE-940')
);

INSERT INTO vulnerabilidad (cve, cve_score) VALUES (
  'CVE-2026-10254', 7.0
);

INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
  (SELECT id FROM activo WHERE direccion='d4:f5:27:b5:cd:67'),
  ( SELECT riesgo_datos.id
    FROM vulnerabilidad,amenaza,riesgo_datos
    WHERE vulnerabilidad.cve='CVE-2025-13254' AND
          amenaza.codigo_cwe='CWE-940' AND
          riesgo_datos.vulnerabilidad_id=vulnerabilidad.id AND
          riesgo_datos.amenaza_id=amenaza.id
  )
);

INSERT INTO amenaza (codigo_cwe, name, prioridad) VALUES (
  'T3','Utilizar datos erróneos y/o poco fiables', 1.0
);

INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (
  (SELECT id FROM vulnerabilidad WHERE cve='CVE-2026-10254'),
  (SELECT id FROM amenaza WHERE codigo_cwe='T3')
);

INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
  (SELECT id FROM activo WHERE direccion='d4:f5:27:94:53:93'),
  (SELECT riesgo_datos.id
    FROM vulnerabilidad,amenaza,riesgo_datos
    WHERE vulnerabilidad.cve='CVE-2026-10254' AND
          amenaza.codigo_cwe='T3' AND
          riesgo_datos.vulnerabilidad_id=vulnerabilidad.id AND
          riesgo_datos.amenaza_id=amenaza.id
  )
);

-- Insertamos una amenaza de prueba
INSERT INTO amenaza (codigo_cwe, name, prioridad) 
VALUES ('CWE-79', 'Cross-site Scripting (XSS)', 5.0);

-- Insertamos una versión de fórmula de prueba
INSERT INTO formula_version (formula_code, version, expression) 
VALUES ('SAGR-M1', 'v1.0', 'severity * frequency');

-- Insertamos el registro en cwe_score usando los IDs anteriores (ambos son ID: 1)
INSERT INTO cwe_score (
  amenaza_id, formula_version_id, 
  severity_component, frequency_component, critical_component, 
  kev_component, cwe_maturity_component, cwe_r10, is_current
) VALUES (1, 1, 5.0, 4.0, 3.0, 2.0, 1.0, 5.0, 1);

-- Intentamos meter EXACTAMENTE la misma combinación activa que en el Paso 1
INSERT INTO cwe_score (
  amenaza_id, formula_version_id, 
  severity_component, frequency_component, critical_component, 
  kev_component, cwe_maturity_component, cwe_r10, is_current
) VALUES (1, 1, 6.0, 5.0, 4.0, 3.0, 2.0, 6.0, 1);

SELECT id, amenaza_id, formula_version_id, is_current, current_key FROM cwe_score;

SELECT 
    a.id AS amenaza_id, 
    a.codigo_cwe, 
    a.name AS nombre_amenaza
FROM amenaza a
WHERE a.id = 1;

SELECT * FROM activo_riesgo;

# Modifica la consulta dentro de tu ruta de /riesgos

    SELECT 
        a.direccion, 
        GROUP_CONCAT(DISTINCT a.nodo SEPARATOR ', ') AS cpe, 
        v.cve AS vulnerabilidad, 
        am.name AS amenaza, 
        v.cve_score AS valor_riesgo
    FROM activo_riesgo ar
    JOIN activo a ON ar.activo_id = a.id
    JOIN riesgo_datos rd ON ar.riesgo_id = rd.id
    JOIN vulnerabilidad v ON rd.vulnerabilidad_id = v.id
    JOIN amenaza am ON rd.amenaza_id = am.id
    GROUP BY a.direccion, v.cve, am.name, v.cve_score;

-- Total vulnerabilidades 
SELECT * FROM nozomi_test_db.vulnerabilidad;

SELECT id, direccion, nodo, prioridad, valor_alcanzable FROM                                              
     activo ORDER BY id;                     
