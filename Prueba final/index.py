import tkinter as tk
from PIL import Image, ImageTk
import serial
import threading
import cv2
import time
import pymongo
import gridfs

# Configuración de la conexión a MongoDB
MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URL = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"

# Conectar a MongoDB
try:
    cliente = pymongo.MongoClient(MONGO_URL, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    cliente.server_info()
    print("Conexión a Mongo exitosa")

    # Seleccionar la base de datos
    db = cliente['nombre_de_tu_base_de_datos']

    # Inicializar GridFS
    fs = gridfs.GridFS(db)

except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo excedido " + str(errorTiempo))
    exit()
except pymongo.errors.ConnectionFailure as errorConexion:
    print("Fallo al conectarse a MongoDB " + str(errorConexion))
    exit()
except Exception as e:
    print("Ocurrió un error: ", str(e))
    exit()

# Configurar el puerto serial
ser = serial.Serial('COM3', 9600, timeout=1)  # Cambiar 'COM10' al puerto correcto

# Crear una ventana tkinter
window = tk.Tk()
window.title("Camara")

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variable global para el factor de zoom
zoom_factor = 1.0

# Variable global para mantener el contador de fotos
contador_fotos = 0

# Crear un label para la cuenta regresiva
countdown_label = tk.Label(window, text="", font=("Helvetica", 48), fg="red")
countdown_label.pack(side="right")

def leer_serial():
    global zoom_factor, contador_fotos
    while True:
        # Leer datos del puerto serial
        mensaje = ser.readline().decode().strip()
        if mensaje.isdigit():
            # Si se recibe un valor numérico, actualizar el factor de zoom
            zoom_factor = 1.0 + int(mensaje) / 1000.0
        elif mensaje == "Boton presionado":
            # Si se recibe el mensaje "Boton presionado", iniciar la cuenta regresiva y programar una foto en 5 segundos
            iniciar_cuenta_regresiva()

# Función para tomar una foto y guardarla en MongoDB
def tomar_foto():
    global contador_fotos
    # Capturar una imagen
    ret, frame = cap.read()
    if ret:
        # Convertir la imagen a bytes
        _, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

        # Guardar la imagen en MongoDB usando GridFS
        file_id = fs.put(img_bytes, filename=f'foto_{contador_fotos}.jpg')
        print(f"Foto guardada en MongoDB con ID: {file_id}")

        # Mostrar la imagen capturada en una ventana
        cv2.imshow('Captura', frame)
        cv2.waitKey(2000)  # Esperar 2 segundos para ver la imagen
        cv2.destroyAllWindows()

def iniciar_cuenta_regresiva():
    global contador_fotos
    contador_fotos += 1

    def cuenta_regresiva(contador):
        if contador >= 0:
            countdown_label.config(text=str(contador))
            window.after(1000, cuenta_regresiva, contador - 1)
        else:
            countdown_label.config(text="")
            tomar_foto()

    cuenta_regresiva(5)

# Crear un hilo para leer mensajes del puerto serial
thread_serial = threading.Thread(target=leer_serial)
thread_serial.start()

# Función para mostrar la imagen de la cámara en la ventana tkinter
def mostrar_camara():
    ret, frame = cap.read()
    if ret:
        # Aplicar zoom al fotograma
        frame_zoomed = cv2.resize(frame, None, fx=zoom_factor, fy=zoom_factor, interpolation=cv2.INTER_LINEAR)
        # Convertir el fotograma a RGB
        frame_rgb = cv2.cvtColor(frame_zoomed, cv2.COLOR_BGR2RGB)
        # Crear una imagen PIL
        img = Image.fromarray(frame_rgb)
        # Convertir la imagen PIL a formato compatible con tkinter
        imgtk = ImageTk.PhotoImage(image=img)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        panel.after(10, mostrar_camara)

# Crear un panel en la ventana para mostrar la imagen de la cámara
panel = tk.Label(window)
panel.pack(side="left")

# Iniciar el proceso de mostrar la imagen de la cámara
mostrar_camara()

# Ajustar el tamaño de la ventana para que coincida con el tamaño de la cámara
window.geometry(f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

# Iniciar el bucle principal de tkinter
window.mainloop()

# Cerrar la conexión a MongoDB cuando se cierre la aplicación
cliente.close()
