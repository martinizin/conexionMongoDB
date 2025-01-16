import concurrent.futures
from pymongo import MongoClient
from bson import ObjectId
import random
import string
from datetime import datetime

# Conexión a MongoDB
def conectar_a_mongo():
    try:
        uri= "Reemplaza por la cadena de conexión del cluster de mongoDB";
        cliente = MongoClient(uri)
        db = cliente['Reemplaza por el nombre de la base de datos']
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

# Funciones CRUD para la prueba
def crear_cliente_prueba(db):
    cliente_data = {
        "nombre": ''.join(random.choices(string.ascii_letters, k=10)),
        "email": ''.join(random.choices(string.ascii_lowercase, k=5)) + "@example.com",
        "telefono": ''.join(random.choices(string.digits, k=10)),
        "direccion": "Calle de Prueba",
        "interacciones": []
    }
    db.clientes.insert_one(cliente_data)

def registrar_interaccion_prueba(db, cliente_id):
    interaccion_data = {
        "cliente_id": ObjectId(cliente_id),
        "fecha": datetime.utcnow(),
        "tipo": random.choice(["llamada", "correo", "reunión"]),
        "descripcion": "Interacción de prueba"
    }
    db.interacciones.insert_one(interaccion_data)

def leer_clientes_prueba(db):
    list(db.clientes.find())

def actualizar_cliente_prueba(db, cliente_id):
    nuevos_datos = {
        "nombre": "Nombre Actualizado",
        "email": "actualizado@example.com",
        "telefono": "0000000000",
        "direccion": "Nueva Dirección"
    }
    db.clientes.update_one({"_id": ObjectId(cliente_id)}, {"$set": nuevos_datos})

def eliminar_cliente_prueba(db, cliente_id):
    db.clientes.delete_one({"_id": ObjectId(cliente_id)})

# Simulación de carga
def prueba_de_carga():
    db = conectar_a_mongo()
    if db is None:
        print("No se pudo conectar a la base de datos.")
        return

    # Crear clientes iniciales para las pruebas
    print("Creando clientes iniciales...")
    cliente_ids = []
    for _ in range(50):  # Crear 50 clientes
        cliente_data = {
            "nombre": ''.join(random.choices(string.ascii_letters, k=10)),
            "email": ''.join(random.choices(string.ascii_lowercase, k=5)) + "@example.com",
            "telefono": ''.join(random.choices(string.digits, k=10)),
            "direccion": "Calle de Prueba",
            "interacciones": []
        }
        resultado = db.clientes.insert_one(cliente_data)
        cliente_ids.append(resultado.inserted_id)

    print("Iniciando prueba de carga...")

    # Función para ejecutar operaciones aleatorias
    def operacion_random():
        operacion = random.choice(["crear", "leer", "actualizar", "eliminar", "interaccion"])
        if operacion == "crear":
            crear_cliente_prueba(db)
        elif operacion == "leer":
            leer_clientes_prueba(db)
        elif operacion == "actualizar":
            cliente_id = random.choice(cliente_ids)
            actualizar_cliente_prueba(db, cliente_id)
        elif operacion == "eliminar":
            cliente_id = random.choice(cliente_ids)
            eliminar_cliente_prueba(db, cliente_id)
        elif operacion == "interaccion":
            cliente_id = random.choice(cliente_ids)
            registrar_interaccion_prueba(db, cliente_id)

    # Ejecutar operaciones concurrentes
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(operacion_random) for _ in range(200)]  # 200 operaciones
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error durante la operación: {e}")

    print("Prueba de carga finalizada.")

if __name__ == "__main__":
    prueba_de_carga()
