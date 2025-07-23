from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# Cadena de conexión a MongoDB
def conectar_a_mongo():
    try:
        uri = "Coloca la cadena de conexión del cluster de mongoDB"
        cliente = MongoClient(uri)
        db = cliente['Nombre de la base de datos']  
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

# Función Crear un cliente
def crear_cliente(db):
    try:
        cliente_data = {
            "nombre": input("Nombre del cliente: "),
            "email": input("Correo electrónico: "),
            "telefono": input("Teléfono: "),
            "direccion": input("Dirección: "),
            "interacciones": []  # Lista vacía para almacenar interacciones
        }
        resultado = db.Clientes.insert_one(cliente_data)
        print(f"Cliente creado con ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"Error al crear cliente: {e}")

# Función leer clientes
def leer_clientes(db):
    try:
        clientes = db.Clientes.find()
        print("Clientes registrados:")
        for cliente in clientes:
            print(cliente)
    except Exception as e:
        print(f"Error al leer clientes: {e}")

# Función actualizar un cliente
def actualizar_cliente(db):
    try:
        cliente_id = input("ID del cliente a actualizar: ")
        nuevos_datos = {
            "nombre": input("Nuevo nombre: "),
            "email": input("Nuevo correo electrónico: "),
            "telefono": input("Nuevo teléfono: "),
            "direccion": input("Nueva dirección: ")
        }
        resultado = db.Clientes.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$set": nuevos_datos}
        )
        if resultado.modified_count > 0:
            print("Cliente actualizado correctamente.")
        else:
            print("No se encontró el cliente o no se realizaron cambios.")
    except Exception as e:
        print(f"Error al actualizar cliente: {e}")

# Función Eliminar un cliente
def eliminar_cliente(db):
    try:
        cliente_id = input("ID del cliente a eliminar: ")
        resultado = db.Clientes.delete_one({"_id": ObjectId(cliente_id)})
        if resultado.deleted_count > 0:
            print("Cliente eliminado correctamente.")
        else:
            print("No se encontró el cliente.")
    except Exception as e:
        print(f"Error al eliminar cliente: {e}")

# Función registrar una interacción
def registrar_interaccion(db):
    try:
        cliente_id = input("ID del cliente para registrar la interacción: ")
        interaccion_data = {
            "cliente_id": ObjectId(cliente_id),
            "fecha": datetime.utcnow(),
            "tipo": input("Tipo de interacción (llamada/correo/reunión): "),
            "descripcion": input("Descripción de la interacción: ")
        }
        resultado = db.interacciones.insert_one(interaccion_data)
        # Opcionalmente, actualiza el campo de interacciones en la colección de clientes
        db.Clientes.update_one(
            {"_id": ObjectId(cliente_id)},
            {"$push": {"interacciones": interaccion_data}}
        )
        print(f"Interacción registrada con ID: {resultado.inserted_id}")
    except Exception as e:
        print(f"Error al registrar interacción: {e}")

# Función leer interacciones de un cliente
def leer_interacciones_cliente(db):
    try:
        cliente_id = input("ID del cliente para ver las interacciones: ")
        interacciones = db.interacciones.find({"cliente_id": ObjectId(cliente_id)})
        print(f"Interacciones del cliente {cliente_id}:")
        for interaccion in interacciones:
            print(interaccion)
    except Exception as e:
        print(f"Error al leer interacciones del cliente: {e}")

# Menú principal para realizar CRUD
def menu():
    db = conectar_a_mongo()
    if db is None:
        print("No se pudo conectar a la base de datos. Saliendo...")
        return
    while True:
        print("\n--- Menú CRUD Clientes e Interacciones ---")
        print("1. Crear cliente")
        print("2. Leer clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Registrar interacción")
        print("6. Leer interacciones de un cliente")
        print("7. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_cliente(db)
        elif opcion == "2":
            leer_clientes(db)
        elif opcion == "3":
            actualizar_cliente(db)
        elif opcion == "4":
            eliminar_cliente(db)
        elif opcion == "5":
            registrar_interaccion(db)
        elif opcion == "6":
            leer_interacciones_cliente(db)
        elif opcion == "7":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()

