import pymongo
import cv2
import gridfs
import time

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

    # Capturar la foto con OpenCV
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        cliente.close()
        exit()

    time.sleep(2)  # Esperar para que la cámara esté lista

    ret, frame = cap.read()

    if ret:
        # Mostrar la imagen capturada en una ventana
        cv2.imshow('Captura', frame)
        cv2.waitKey(2000)  # Esperar 2 segundos para ver la imagen
        cv2.destroyAllWindows()

        # Convertir la imagen a bytes
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        # Guardar la imagen en MongoDB usando GridFS
        file_id = fs.put(img_bytes, filename='foto.jpg')
        print("Foto guardada en MongoDB con ID:", file_id)
    else:
        print("No se pudo capturar la imagen")

    # Liberar la cámara
    cap.release()

    # Cerrar la conexión
    cliente.close()

except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo excedido " + str(errorTiempo))
except pymongo.errors.ConnectionFailure as errorConexion:
    print("Fallo al conectarse a MongoDB " + str(errorConexion))
except Exception as e:
    print("Ocurrió un error: ", str(e))
