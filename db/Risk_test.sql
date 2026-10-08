USE nozomi_test_db;

-- SELECT * FROM nodo_cliente;
-- SELECT * FROM cliente;

-- SELECT
--   cliente.email,
--   activo.direccion, vulnerabilidad.cve, amenaza.codigo_cwe,
--   activo.prioridad , vulnerabilidad.cve_score , amenaza.prioridad,
--   activo.prioridad + vulnerabilidad.cve_score + amenaza.prioridad - 3 AS riesgo
-- FROM cliente,activo,vulnerabilidad,amenaza,riesgo_datos,activo_riesgo
-- WHERE activo.cliente_id = cliente.id AND
--       activo_riesgo.activo_id = activo.id AND
--       activo_riesgo.riesgo_id = riesgo_datos.id AND
--       riesgo_datos.amenaza_id = amenaza.id AND
--       riesgo_datos.vulnerabilidad_id = vulnerabilidad.id;

-- SELECT * FROM riesgo WHERE direccion='d4:f5:27:94:53:93';
-- SELECT * FROM riesgo;

SELECT activo.nodo , vulnerabilidad.cve
FROM activo
INNER JOIN vulnerabilidad ON activo.id = vulnerabilidad.id
WHERE vulnerabilidad.cve = 'CVE-2025-13254';

SELECT activo.nodo, vulnerabilidad.cve
FROM activo
INNER JOIN vulnerabilidad ON activo.id = vulnerabilidad.id
WHERE vulnerabilidad.cve = 'CVE-2022-4450';

SELECT * FROM activo WHERE nodo = 'Servidor Siemens de DA';
SELECT * FROM activo WHERE direccion = 'd4:45:27:94:53:93';

SELECT activo.nodo, vulnerabilidad.cve
FROM activo
INNER JOIN vulnerabilidad ON activo.id = vulnerabilidad.id
WHERE activo.id = '18';

SELECT *
FROM vulnerabilidad 
LEFT JOIN activo 
ON vulnerabilidad.id = activo.id

WHERE activo.id IS NULL;

SHOW INDEX FROM activo;

SELECT direccion, COUNT(*) AS cantidad
FROM activo
GROUP BY direccion
HAVING COUNT(*) > 1;

UPDATE activo SET prioridad=5 WHERE direccion='192.168.12.2';

SELECT DISTINCT direccion FROM activo;

SELECT DISTINCT prioridad FROM activo WHERE direccion='192.168.12.2';

SELECT vulnerabilidad.cve, amenaza.codigo_cwe, amenaza.name
FROM vulnerabilidad,amenaza,activo,activo_riesgo,riesgo_datos
WHERE activo.direccion='d4:45:27:94:53:93' AND
      activo.nodo='cpe:/h:siemens:s7-410:-:-:-' AND
      activo_riesgo.activo_id = activo.id AND
      activo_riesgo.riesgo_id = riesgo_datos.id AND
      riesgo_datos.amenaza_id = amenaza.id AND
      riesgo_datos.vulnerabilidad_id = vulnerabilidad.id;

