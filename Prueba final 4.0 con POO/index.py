import tkinter as tk
from PIL import Image, ImageTk
import serial
import threading
import cv2
import time
import pymongo
import gridfs

class CamaraApp:
    def __init__(self):
        # Configuración de la conexión a MongoDB
        self.MONGO_HOST = "localhost"
        self.MONGO_PUERTO = "27017"
        self.MONGO_TIEMPO_FUERA = 1000
        self.MONGO_URL = "mongodb://" + self.MONGO_HOST + ":" + self.MONGO_PUERTO + "/"

        # Conectar a MongoDB
        try:
            self.cliente = pymongo.MongoClient(self.MONGO_URL, serverSelectionTimeoutMS=self.MONGO_TIEMPO_FUERA)
            self.cliente.server_info()
            print("Conexión a Mongo exitosa")
            # Seleccionar la base de datos
            self.db = self.cliente['Base_de_datos']
            # Inicializar GridFS
            self.fs = gridfs.GridFS(self.db)
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
        self.ser = serial.Serial('COM6', 9600, timeout=1)  # Cambiar 'COM10' al puerto correcto

        # Crear una ventana tkinter
        self.window = tk.Tk()
        self.window.title("Cámara")

        # Inicializar la cámara
        self.cap = cv2.VideoCapture(0)

        # Variable global para el factor de zoom
        self.zoom_factor = 1.0

        # Variable global para mantener el contador de fotos
        self.contador_fotos = 0

        # Crear un label para la cuenta regresiva
        self.countdown_label = tk.Label(self.window, text="", font=("Helvetica", 48), fg="red")
        self.countdown_label.pack(side="right")

        # Crear un hilo para leer mensajes del puerto serial
        self.thread_serial = threading.Thread(target=self.leer_serial)
        self.thread_serial.start()

        # Función para mostrar la imagen de la cámara en la ventana tkinter
        def mostrar_camara():
            ret, frame = self.cap.read()
            if ret:
                # Aplicar zoom al fotograma
                frame_zoomed = cv2.resize(frame, None, fx=self.zoom_factor, fy=self.zoom_factor, interpolation=cv2.INTER_LINEAR)
                # Convertir el fotograma a RGB
                frame_rgb = cv2.cvtColor(frame_zoomed, cv2.COLOR_BGR2RGB)
                # Crear una imagen PIL
                img = Image.fromarray(frame_rgb)
                # Convertir la imagen PIL a formato compatible con tkinter
                imgtk = ImageTk.PhotoImage(image=img)
                self.panel.imgtk = imgtk
                self.panel.config(image=imgtk)
                self.panel.after(10, mostrar_camara)

        # Crear un panel en la ventana para mostrar la imagen de la cámara
        self.panel = tk.Label(self.window)
        self.panel.pack(side="left")

        # Iniciar el proceso de mostrar la imagen de la cámara
        mostrar_camara()

        # Ajustar el tamaño de la ventana para que coincida con el tamaño de la cámara
        self.window.geometry(f"{int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

        # Iniciar el bucle principal de tkinter
        self.window.mainloop()

        # Cerrar la conexión a MongoDB cuando se cierre la aplicación
        self.cliente.close()

    # Función para leer datos del puerto serial
    def leer_serial(self):
        while True:
            # Leer datos del puerto serial
            mensaje = self.ser.readline().decode().strip()
            if mensaje.isdigit():
                # Si se recibe un valor numérico, actualizar el factor de zoom
                self.zoom_factor = 1.0 + int(mensaje) / 1000.0
            elif mensaje == "Boton presionado":
                # Si se recibe el mensaje "Boton presionado", iniciar la cuenta regresiva y programar una foto en 5 segundos
                self.iniciar_cuenta_regresiva()

    # Función para iniciar la cuenta regresiva y tomar una foto después de 5 segundos
    def iniciar_cuenta_regresiva(self):
        self.contador_fotos += 1

        def cuenta_regresiva(contador):
            if contador >= 0:
                self.countdown_label.config(text=str(contador))
                self.window.after(1000, cuenta_regresiva, contador - 1)
            else:
                self.countdown_label.config(text="")
                self.tomar
