import mysql.connector

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

def GetActivoId(direccion, nodo):
    Command="""
        SELECT id FROM activo
        WHERE direccion='""" + direccion + """' AND
              nodo='""" + nodo + """'
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

def InsertVulnerabilidad(cve, activo_id):
    Command="""
        INSERT INTO vulnerabilidad (cve, activo_id ) VALUES (
            '""" + cve + """',
            '""" + str(activo_id) + """'
        );
    """
    return RunInsert(Command)


connection = mysql.connector.connect(
    host = "localhost",
    user = "carlos",
    password = "123",
    database = "nozomi_test_db"
)