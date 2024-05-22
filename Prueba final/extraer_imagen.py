import pymongo
import cv2
import gridfs
import numpy as np
from bson import ObjectId

# Configuración de la conexión a MongoDB
MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URL = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"

try:
    cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    cliente.server_info()
    print("Conexión a Mongo exitosa")

    # Seleccionar la base de datos
    db = cliente['Base_de_datos']

    # Inicializar GridFS
    fs = gridfs.GridFS(db)

    # Buscar la imagen guardada en GridFS usando su ID
    file_id = ObjectId("664d483ea34ebde5b2c389dc")  # Reemplaza con el ID correcto de la foto guardada
    grid_out = fs.get(file_id)

    # Leer los datos de la imagen como bytes
    img_bytes = grid_out.read()

    # Convertir los bytes de la imagen a un array de NumPy
    img_array = np.frombuffer(img_bytes, dtype=np.uint8)

    # Decodificar el array de NumPy a una imagen utilizando OpenCV
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Mostrar la imagen
    cv2.imshow('Imagen desde MongoDB', img)
    cv2.waitKey(0)  # Esperar hasta que se presione una tecla
    cv2.destroyAllWindows()

    # Cerrar la conexión
    cliente.close()

except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo excedido " + str(errorTiempo))
except pymongo.errors.ConnectionFailure as errorConexion:
    print("Fallo al conectarse a MongoDB " + str(errorConexion))
except Exception as e:
    print("Ocurrió un error: ", str(e))
