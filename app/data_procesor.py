import mysql.connector
import csv

def SelectId(Command):
    cursor = connection.cursor()
    try:
        cursor.execute(Command)
        Id=cursor.fetchone()
        if Id is not None:
            Id=Id[0]
    except:
        raise
        Id=None
    cursor.close()
    return Id

def GetClienteId(email):
    Command="""
        SELECT id FROM cliente
        WHERE email='""" + email + """'
    """
    return SelectId(Command)

def GetActivoId(direccion, nodo):
    Command="""
        SELECT id FROM activo
        WHERE direccion='""" + direccion + """' AND
              nodo='""" + nodo + """'
    """
    return SelectId(Command)

def GetVulnerabilidadId(CVE):
    Command="""
        SELECT id FROM vulnerabilidad WHERE cve='""" + CVE + """'
    """
    return SelectId(Command)

def GetAmenazaId(CWE):
    Command="""
        SELECT id FROM amenaza WHERE codigo_cwe='""" + CWE + """'
    """
    return SelectId(Command)

def GetRiesgoId(VulnerabilidadId, AmenazaId):
    if VulnerabilidadId is not None and AmenazaId is not None:
        Command="""
            SELECT id FROM riesgo_datos
            WHERE vulnerabilidad_id='""" + str(VulnerabilidadId) + """' AND
                amenaza_id='""" + str(AmenazaId) + """'
        """
        return SelectId(Command)

def RunInsert(Command):
    cursor = connection.cursor()
    try:
        cursor.execute(Command)
        RowCount=cursor.rowcount
    except:
        RowCount=0

    cursor.close()
    return RowCount

def InsertActivo(direccion, nodo):
    Command="""
        INSERT INTO activo (direccion, nodo, cliente_id) VALUES (
            '""" + direccion + """',
            '""" + nodo + """',
            (SELECT id FROM cliente WHERE email='tester@example.com')
        );
    """
    return RunInsert(Command)

def InsertVulnerabilidad(cve, score):
    Command="""
        INSERT INTO vulnerabilidad (cve, cve_score) VALUES (
            '""" + cve + """',
            '""" + score + """'
        );
    """
    return RunInsert(Command)

def InsertAmenaza(cwe, name):
    Command="""INSERT INTO amenaza (codigo_cwe, name) VALUES (
                    '""" + cwe + """',
                    '""" + name.replace("'", "\\'") + """'
                );
    """
    return RunInsert(Command)            

# Ingresa vulnerabilidad_id y amenaza_id a Tbl riesgo_datos 
# Riesgo INSERT RESULT: 1
def InsertRiesgo(VulnerabilidadId, AmenazaId):
    Command="""INSERT INTO riesgo_datos (vulnerabilidad_id, amenaza_id) VALUES (
                    """ + str(VulnerabilidadId) + """,
                    """ + str(AmenazaId) + """
                );    
    """
    return RunInsert(Command)            

#Activo/Riesgo INSERT RESULT: 1
def InsertActivoRiesgo(ActivoId, RiesgoId):
################################################################################################
    Command="""INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
                    """ + str(ActivoId) + """,
                    """ + str(RiesgoId) + """
                );    
    """
###############################################################################################
    return RunInsert(Command)            

def InsertRisk(activo, vulnerabilidad, amenaza):
    Command="""
        INSERT INTO activo_riesgo (activo_id, riesgo_id) VALUES (
        (SELECT id FROM activo WHERE direccion='""" + activo + """'),
        (SELECT riesgo_datos.id
            FROM vulnerabilidad,amenaza,riesgo_datos
            WHERE vulnerabilidad.cve='""" + vulnerabilidad + """' AND
                amenaza.codigo_cwe='""" + amenaza + """' AND
                riesgo_datos.vulnerabilidad_id=vulnerabilidad.id AND
                riesgo_datos.amenaza_id=amenaza.id
        )
    );
    """
    return RunInsert(Command)

def TestInsert():
    RowCount=InsertRisk(
        activo = "30:2f:1e:21:4d:3c",
        vulnerabilidad = "CVE-2025-13254",
        amenaza = "T1"
    )
    print("Records inserted (existing): ",RowCount)
    activo = "d4:f5:27:71:d4:3e"
    vulnerabilidad = "CVE-2023-51440"
    amenaza = "CWE-940"
    RowCount=InsertRisk(activo, vulnerabilidad, amenaza)
    print("Records inserted (nonexistent): ",RowCount)
    if RowCount==0:
        RowCount=InsertActivo(activo)
        print("Activo records inserted: ",RowCount)

    connection.commit()

def TestGetId():
    Server1=GetActivoId("30:2f:1e:21:4d:3c")
    print(Server1)
    if Server1 is None:
        print("No existe")
    Server2=GetActivoId("d4:f5:27:71:d4:3e")
    print(Server2)
    if Server2 is None:
        print("No existe")
    Vulnerabilidad1=GetVulnerabilidadId("CVE-2025-13254")
    print(Vulnerabilidad1)
    Vulnerabilidad2=GetVulnerabilidadId("CVE-NONE-NONE")
    print(Vulnerabilidad2)
    Amenaza1=GetAmenazaId("T1")
    print(Amenaza1)
    Amenaza2=GetAmenazaId("Tnone")
    print(Amenaza2)
    Riesgo1=GetRiesgoId(Vulnerabilidad1, Amenaza1)
    print(Riesgo1)
    Riesgo2=GetRiesgoId(12345678, Amenaza1)
    print(Riesgo2) 

connection = mysql.connector.connect(
    host = "localhost",
    user = "carlos",
    password = "123",
    database = "nozomi_test_db"
);

File="export_node_cves_Datecsa.csv"
File="/home/carlos/Desktop/YouTubeTutorial/data/"+File

#print(File)


#### Tarea ####

with open(File, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        direccion = row["node_id"].strip()
        nodos = row["matching_cpes"]
        cve = row["cve"].strip()
        score = row["cve_score"].strip()
        codigo_cwe = "CWE-"+row["cwe_id"].strip()
        name = row["cwe_name"].strip()

        
        VulnerabilidadId=GetVulnerabilidadId(cve)
        if VulnerabilidadId is None:
            estado_cve = "NO EXISTE"
        else:
            estado_cve = "EXISTE("+str(VulnerabilidadId)+")"

        
        AmenazaId=GetAmenazaId(codigo_cwe)
        if AmenazaId is None:
            estado_cwe = "NO EXISTE"
        else:
            estado_cwe = "EXISTE("+str(AmenazaId)+")"       


        print(f"{cve} {estado_cve} {codigo_cwe} {estado_cwe}")

        if VulnerabilidadId is None:
            RowCount=InsertVulnerabilidad(cve, score)
            print("Vulnerabilidad INSERT RESULT:",RowCount)
            if RowCount==1:
                VulnerabilidadId=GetVulnerabilidadId(cve)

        if AmenazaId is None:
            RowCount=InsertAmenaza(codigo_cwe, name)
            print("Amenaza INSERT RESULT:",RowCount)
            if RowCount==1: 
                AmenazaId=GetAmenazaId(codigo_cwe)

        if VulnerabilidadId is None or AmenazaId is None:
            # Riesgo no puede existir
            continue

        #estado_cwe = "EXISTE" if GetAmenazaId(codigo_cwe) else "NO EXISTE"
        RiesgoId=GetRiesgoId(VulnerabilidadId, AmenazaId)
        if RiesgoId is None:
            estado_riesgo = "NO EXISTE"
        else:
            estado_riesgo = "EXISTE("+str(RiesgoId)+")"    




        print(f"RIESGO {cve}:{codigo_cwe} {estado_riesgo}")

        # Inserta riesgo: CVE + CWE en ActivoId
        if RiesgoId is None:
            RowCount=InsertRiesgo(VulnerabilidadId,AmenazaId)
            print("Riesgo INSERT RESULT:",RowCount)
            if RowCount==1:
                RiesgoId=GetRiesgoId(VulnerabilidadId, AmenazaId)
        if RiesgoId is None:
            continue

        # Guardamos los estados en variables para que sea más limpio
        nodos = nodos.split(",")
        for nodo in nodos:
            nodo = nodo.strip()
            partes = nodo.split(':')
            if len(partes) >= 4:
                nodo=(f"{partes[2]}:{partes[3]}")
            ActivoId=GetActivoId(direccion, nodo)
            if ActivoId is None:
                estado_ip = "NO EXISTE"
            else:
                estado_ip = "EXISTE("+str(ActivoId)+")"
            print(f"{direccion} {nodo} {estado_ip}")
            if ActivoId is None:
                RowCount=InsertActivo(direccion, nodo)
                print("Activo INSERT RESULT:",RowCount)
                if RowCount == 1:
                    ActivoId = GetActivoId(direccion, nodo)
            if ActivoId is None:
                continue
            RowCount=InsertActivoRiesgo(ActivoId, RiesgoId)
            print("Activo/Riesgo INSERT RESULT:",RowCount)
            break


def extraer_cpes(ruta, columna="matching_cpes"):
    resultados = []
    try:
        with open(ruta, mode='r', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            
            for fila in lector:
                celda = fila.get(columna)
                if celda:
                    # 1. Tomamos el primer CPE si hay varios en la celda
                    primer_cpe = celda.split(',')[0].strip()
                    
                    # 2. Extraemos fabricante y producto
                    partes = primer_cpe.split(':')
                    if len(partes) >= 4:
                        resultados.append(f"{partes[2]}:{partes[3]}")
                                
        return resultados

    except Exception as e:
        return [f"Error: {e}"]
        
# Ejecución
lista_cpes = extraer_cpes(File)

# Visualizar los primeros 22 resultados para verificar
#for cpe in lista_cpes[:22]:
    #print(cpe)


connection.commit()

mycursor = connection.cursor()

mycursor.execute("ALTER TABLE activo ADD COLUMN valor_direccion INT NULL;")

myresult = mycursor.fetchall()

#for x in myresult:
 # print(x)


