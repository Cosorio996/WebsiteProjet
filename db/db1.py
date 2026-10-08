from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import os
import csv
import io

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
)
app.secret_key = "123"

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="carlos",
        password="123",
        database="nozomi_test_db"
    )

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            ROUND(SUM(riesgo_valor), 2) AS risk_score_total,
            ROUND(AVG(riesgo_valor), 2) AS risk_score_promedio,
            CAST(MAX(riesgo_valor) AS SIGNED) AS risk_score_maximo,       
            COUNT(*) AS total_riesgos
        FROM riesgo
    """)
    resumen = cursor.fetchone()
    cursor.close()

    return render_template(
        'dashboard.html',
        risk_score_total=resumen["risk_score_total"] or 0,
        risk_score_promedio=resumen["risk_score_promedio"] or 0,
        risk_score_maximo=resumen["risk_score_maximo"] or 0,
        total_riesgos=resumen["total_riesgos"] or 0
    )

# -----------------------------
# LISTAR DIRECCIONES UNICAS
# -----------------------------
@app.route("/direcciones")
def ver_direcciones():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT direccion, MAX(prioridad) AS prioridad
        FROM activo
        GROUP BY direccion                    
    """
    
    cursor.execute(query)
    direcciones = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("direcciones.html", direcciones=direcciones)


# -----------------------------
# GUARDAR VALOR DE DIRECCION
# -----------------------------
@app.route("/direcciones/guardar", methods=["POST"])
def guardar_valor_direccion_desde_lista():
    direccion = request.form.get("direccion")
    prioridad = request.form.get("prioridad")

    try:
        if not direccion:
            return "Error: debe seleccionar una dirección", 400

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE activo
            SET prioridad = NULL
            WHERE direccion = %s
        """
        cursor.execute(query, (direccion,))
        connection.commit()

    except Exception as e:
        return f"Error al guardar valor de dirección: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

    return redirect(url_for("ver_direcciones"))

# -----------------------------
# GUARDAR VALOR DE ACTIVOS
# -----------------------------

@app.route("/activos", methods=["GET"])
def ver_activos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT a.id, a.direccion, REPLACE(a.nodo, 'siemens:', '') AS nodo, a.prioridad, a.valor_alcanzable, a.firmware_version
        FROM activo a
        WHERE a.nodo = CASE a.direccion
            WHEN '192.168.12.2' THEN 'siemens:s7-410'
            WHEN 'd4:f5:27:94:53:93' THEN 'siemens:scalance_xc208'
            ELSE a.nodo
        END
        ORDER BY a.direccion
    """
    cursor.execute(query)
    activos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("activos.html", activos=activos)

@app.route("/activos/guardar_lista", methods=["POST"])
def guardar_prioridad_activo_desde_lista():
    activo_id = request.form.get("activo_id")
    prioridad = request.form.get("prioridad")
    # 1. Capturar el nuevo campo enviado desde el formulario HTML
    valor_alcanzable = request.form.get("valor_alcanzable") 

    try:
        if not activo_id:
            return "Error: debe seleccionar un activo", 400

        # 2. Validar que el nuevo campo no venga vacío
        if prioridad is None or prioridad == "" or valor_alcanzable is None or valor_alcanzable == "":
            return "Error: debe ingresar ambos valores", 400

        activo_id = int(activo_id)
        prioridad = float(prioridad)        # Cambiado a float si usas DECIMAL(12,2)
        valor_alcanzable = float(valor_alcanzable) # Convertir a número con decimales

        # Rango de validación (ajusta los límites si es necesario)
        if prioridad < 0 or prioridad > 10 or valor_alcanzable < 0 or valor_alcanzable > 10:
            return "Error: los valores deben estar entre 0 y 10", 400

        connection = get_connection()
        cursor = connection.cursor()

        # 3. Modificar el UPDATE para incluir la nueva columna
        query = """
            UPDATE activo
            SET prioridad = %s,
                valor_alcanzable = %s
            WHERE id = %s
        """
        # 4. Pasar los tres parámetros en orden correcto a execute()
        cursor.execute(query, (prioridad, valor_alcanzable, activo_id))
        connection.commit()

    except Exception as e:
        return f"Error al guardar: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

    return redirect(url_for("ver_activos"))

# -----------------------------
# LISTAR AMENAZAS UNICAS
# -----------------------------
@app.route("/amenazas")
def ver_amenazas():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT name, MAX(prioridad) AS prioridad
        FROM amenaza
        GROUP BY name
    """
    
    cursor.execute(query)
    amenazas = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("amenazas.html", amenazas=amenazas)


# -----------------------------
# GUARDAR VALOR DE AMENAZA
# -----------------------------
@app.route("/amenazas/guardar", methods=["POST"])
def guardar_valor_amenaza_desde_lista():
    name = request.form.get("name")
    prioridad = request.form.get("prioridad")

    try:
        if not name:
            return "Error: debe seleccionar una amenaza", 400

        if prioridad is None or prioridad == "":
            return "Error: debe ingresar un valor", 400

        prioridad = int(prioridad)

        if prioridad < 1 or prioridad > 5:
            return "Error: el valor debe estar entre 1 y 5", 400

        connection = get_connection()
        cursor = connection.cursor()

        query = """
            UPDATE amenaza
            SET prioridad = %s
            WHERE name = %s
        """
        cursor.execute(query, (prioridad, name))
        connection.commit()

    except Exception as e:
        return f"Error al guardar valor de amenaza: {e}", 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

    return redirect(url_for("ver_amenazas"))


@app.route("/riesgos")
def ver_riesgos():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            direccion,
            GROUP_CONCAT(DISTINCT nodo ORDER BY nodo SEPARATOR ', ') AS nodo,
            cve,
            GROUP_CONCAT(DISTINCT name ORDER BY name SEPARATOR ', ') AS name,
            ROUND(MAX(riesgo_valor), 2) AS riesgo_valor
        FROM riesgo
        GROUP BY direccion, cve
        ORDER BY direccion, cve
    """
    cursor.execute(query)
    riesgos = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("riesgos.html", riesgos=riesgos)
        

#@app.route('/')

def export_riesgos(csv_file):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM riesgo"
    cursor.execute(query)
    riesgos = cursor.fetchall()

    csv=open(csv_file,"w")
    csv.write("direccion,nodo,cve,name,riesgo_valor")
    csv.write("\n")

    for riesgo in riesgos:
        csv.write(
           riesgo["direccion"]+','+
           riesgo["nodo"]+','+
           riesgo["cve"]+','+
           riesgo["name"]+','+
           riesgo["riesgo_valor"]
        )
        csv.write("\n")
    csv.close()

    cursor.close()
    connection.close()


# -----------------------------
# CARGA DE CSV DE VULNERABILIDADES
# -----------------------------
@app.route("/activos/cargar_csv", methods=["POST"])
def cargar_csv():
    if "csv_file" not in request.files:
        flash("No se seleccionó ningún archivo", "danger")
        return redirect(url_for("ver_activos"))

    file = request.files["csv_file"]
    if file.filename == "":
        flash("No se seleccionó ningún archivo", "danger")
        return redirect(url_for("ver_activos"))

    if not file.filename.endswith(".csv"):
        flash("El archivo debe ser CSV", "danger")
        return redirect(url_for("ver_activos"))

    try:
        stream = io.StringIO(file.stream.read().decode("utf-8"), newline=None)
        reader = csv.DictReader(stream)

        # Validar que el CSV tiene las columnas requeridas
        required_columns = {"node_id", "matching_cpes", "cve", "cve_score", "cwe_id", "cwe_name"}
        if reader.fieldnames is None:
            flash("El archivo CSV está vacío o no tiene encabezados", "danger")
            return redirect(url_for("ver_activos"))

        missing_columns = required_columns - set(reader.fieldnames)
        if missing_columns:
            flash(f"Formato incorrecto. Faltan columnas: {', '.join(missing_columns)}", "danger")
            return redirect(url_for("ver_activos"))

        connection = get_connection()
        cursor = connection.cursor()

        inserted = 0
        skipped = 0
        for row in reader:
            direccion = row["node_id"].strip()
            nodos = row["matching_cpes"]
            cve = row["cve"].strip()
            score = row["cve_score"].strip()
            codigo_cwe = "CWE-" + row["cwe_id"].strip()
            name = row["cwe_name"].strip()

            # Verificar si la vulnerabilidad ya existe
            cursor.execute("SELECT id FROM vulnerabilidad WHERE cve = %s", (cve,))
            vuln = cursor.fetchone()
            if vuln is not None:
                skipped += 1
                continue  # Saltar si ya existe
            cursor.execute(
                "INSERT INTO vulnerabilidad (cve, cve_score) VALUES (%s, %s)",
                (cve, score)
            )
            vuln_id = cursor.lastrowid

            # Verificar si la amenaza ya existe
            cursor.execute("SELECT id FROM amenaza WHERE codigo_cwe = %s", (codigo_cwe,))
            amen = cursor.fetchone()
            if amen is not None:
                skipped += 1
                continue  # Saltar si ya existe
            cursor.execute(
                "INSERT INTO amenaza (codigo_cwe, name) VALUES (%s, %s)",
                (codigo_cwe, name)
            )
            amen_id = cursor.lastrowid

            # Insertar riesgo_datos
            cursor.execute(
                "INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (%s, %s)",
                (vuln_id, amen_id)
            )
            riesgo_id = cursor.lastrowid

            # Procesar nodos (CPEs)
            nodos_list = nodos.split(",")
            hardware_cpes = []
            firmware_cpes = []

            for nodo in nodos_list:
                nodo = nodo.strip()
                partes = nodo.split(":")
                if len(partes) >= 4:
                    nodo_name = f"{partes[2]}:{partes[3]}"
                    # Extraer versión del firmware si existe
                    firmware_version = partes[4] if len(partes) > 4 and partes[4] != "-" else None
                    # Clasificar por nombre (contiene "firmware" = firmware)
                    if "firmware" in nodo_name.lower():
                        firmware_cpes.append((nodo_name, firmware_version))
                    else:
                        hardware_cpes.append((nodo_name, firmware_version))

            # Seleccionar submodelo preciso de hardware
            # Si hay un CPE más específico (ej: s7-410 vs s7-400), tomar el preciso
            selected_hardware = None
            if hardware_cpes:
                # Buscar el CPE más específico (el que tenga un nombre más largo o contenga otro)
                # Por ahora, tomar el último encontrado (asumimos que el preciso viene después)
                # Mejor heurística: si hay un CPE que contiene a otro, tomar el contenido
                for i, (nombre, ver) in enumerate(hardware_cpes):
                    for j, (otro_nombre, otro_ver) in enumerate(hardware_cpes):
                        if i != j and nombre in otro_nombre and nombre != otro_nombre:
                            # nombre es más genérico, otro_nombre es más preciso
                            selected_hardware = (otro_nombre, otro_ver)
                            break
                    if selected_hardware:
                        break
                if not selected_hardware:
                    # Si no hay submodelo preciso, tomar el genérico
                    selected_hardware = hardware_cpes[0]

            # Procesar hardware seleccionado
            if selected_hardware:
                nodo, _ = selected_hardware
                # Buscar firmware asociado a este hardware
                # El firmware puede tener nombre diferente (ej: scalance_xc208 -> scalance_num2firmware)
                # Tomar la versión del firmware que aparece en la misma fila
                firmware_version_for_hardware = None
                if firmware_cpes:
                    # Si hay un solo firmware, usar ese
                    if len(firmware_cpes) == 1:
                        firmware_version_for_hardware = firmware_cpes[0][1]
                    else:
                        # Si hay múltiples firmwares, buscar por nombre similar
                        for fw_nodo, fw_ver in firmware_cpes:
                            if nodo in fw_nodo or fw_nodo.replace('_firmware', '') in nodo:
                                firmware_version_for_hardware = fw_ver
                                break
                        # Si no se encontró por nombre, usar el primero
                        if firmware_version_for_hardware is None:
                            firmware_version_for_hardware = firmware_cpes[0][1]

                cursor.execute(
                    "SELECT id FROM activo WHERE direccion = %s AND nodo = %s",
                    (direccion, nodo)
                )
                activo = cursor.fetchone()
                if activo is None:
                    cursor.execute(
                        "INSERT INTO activo (direccion, nodo, firmware_version, valor_alcanzable, cliente_id) VALUES (%s, %s, %s, 0.00, (SELECT id FROM cliente WHERE email='tester@example.com'))",
                        (direccion, nodo, firmware_version_for_hardware)
                    )
                    activo_id = cursor.lastrowid
                else:
                    activo_id = activo[0]

                # Insertar activo_riesgo
                cursor.execute(
                    "INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (%s, %s)",
                    (activo_id, riesgo_id)
                )
                inserted += 1

            # Procesar firmware
            for nodo, firmware_version in firmware_cpes:
                cursor.execute(
                    "SELECT id FROM activo WHERE direccion = %s AND nodo = %s",
                    (direccion, nodo)
                )
                activo = cursor.fetchone()
                if activo is None:
                    cursor.execute(
                        "INSERT INTO activo (direccion, nodo, firmware_version, valor_alcanzable, cliente_id) VALUES (%s, %s, %s, 0.00, (SELECT id FROM cliente WHERE email='tester@example.com'))",
                        (direccion, nodo, firmware_version)
                    )
                    activo_id = cursor.lastrowid
                else:
                    activo_id = activo[0]

                # Insertar activo_riesgo
                cursor.execute(
                    "INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (%s, %s)",
                    (activo_id, riesgo_id)
                )
                inserted += 1

        connection.commit()
        cursor.close()
        connection.close()

        flash(f"CSV cargado. {inserted} relaciones nuevas, {skipped} omitidas (ya existían).", "success")

    except Exception as e:
        flash(f"Error al procesar el CSV: {e}", "danger")

    return redirect(url_for("ver_activos"))


if __name__ == "__main__":
    app.run(debug=True)
