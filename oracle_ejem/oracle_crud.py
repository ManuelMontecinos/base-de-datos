# Importamos librerias
import oracledb
import os
from dotenv import load_dotenv
#Cargamos variables de entorno
load_dotenv()
#Definimos valores gracias a las variables de entorno
username = os.getenv("ORACLE_USER")
dsn = os.getenv("ORACLE_DSN")
password = os.getenv("ORACLE_PASSWORD")
#Creamos una conexion reutilizable
def get_connection():
    return oracledb.connect(user=username, password=password, dsn=dsn)

#Funcion para crear una tabla


def create_table() -> None:

    ddl = (
    "CREATE TABLE mems_personas ("
    "rut VARCHAR2(50) PRIMARY KEY,"
    "nombres VARCHAR2(200),"
    "apellidos VARCHAR2(200),"
    "fecha_nacimiento DATE,"
    "cod_area VARCHAR2(20),"
    "numero_telefono VARCHAR2(50)"
    ")"
    )
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl)
                print("Tabla 'personas' creada.")
            conn.commit()    
    except oracledb.DatabaseError as e:
        err = e
        print(f"No se pudo crear la tabla: {err}")


create_table()


from datetime import datetime 

#Create
def create_persona(rut=None, nombres=None, apellidos=None, fecha_nacimiento=None, cod_area=None, numero_telefono=None):
    sql = (
    "INSERT INTO personas (rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono) "
    "VALUES (:rut, :nombres, :apellidos, :fecha_nacimiento, :cod_area, :numero_telefono)"
    )
    bind_fecha = None
    if fecha_nacimiento: 
        bind_fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, {
                "rut": rut,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": bind_fecha,
                "cod_area": cod_area,
                "numero_telefono": numero_telefono,
                })
        conn.commit()
    print(f"Persona con RUT={rut} creada.")




#read

def read_persona(rut: str):
    sql = "SELECT * FROM personas WHERE rut =: rut"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, {"rut": rut})
            row = cur.fetchone()
            if not row:
return None
rut, nombres, apellidos, fecha_nacimiento, cod_area, numero_telefono = row
return {
"rut": rut,
"nombres": nombres,
"apellidos": apellidos,
"fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else None,
"cod_area": cod_area,
"numero_telefono": numero_telefono,
}


