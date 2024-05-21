import serial
import time
import cv2
import tkinter as tk
from PIL import Image, ImageTk


# Configurar la conexión serial con el Arduino (ajusta el puerto si es necesario)
arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Esperar para establecer la conexión


# Función para enviar el comando de inicio de conteo al Arduino
def send_command():
    arduino.write(b'C')  # Enviar el comando para iniciar el conteo
    print("Comando enviado")


# Función para capturar una foto desde la cámara
def take_photo():
    cap = cv2.VideoCapture(0)  # Abrir la cámara
    ret, frame = cap.read()  # Capturar un frame de la cámara
    cap.release()  # Liberar la cámara
    cv2.imwrite("photo.jpg", frame)  # Guardar la foto como 'photo.jpg'
    print("Foto tomada")


# Crear una ventana con un botón para tomar la foto
root = tk.Tk()
root.title("Control de Cámara y Conteo")

# Crear un botón para iniciar el conteo
button_count = tk.Button(root, text="Iniciar Conteo", command=send_command)
button_count.pack(pady=20)

# Crear un botón para tomar la foto
button_photo = tk.Button(root, text="Tomar Foto", command=take_photo)
button_photo.pack(pady=10)

# Función para mostrar la cámara en la ventana
def show_camera():
    cap = cv2.VideoCapture(0)  # Abrir la cámara
    ret, frame = cap.read()  # Capturar un frame de la cámara
    cap.release()  # Liberar la cámara
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir el frame a RGB
    img = Image.fromarray(frame)  # Crear una imagen desde el frame
    img = ImageTk.PhotoImage(image=img)  # Convertir la imagen para Tkinter
    label_camera.imgtk = img  # Guardar la imagen para evitar que sea recolectada por el recolector de basura
    label_camera.config(image=img)  # Mostrar la imagen en la etiqueta
    label_camera.after(10, show_camera)  # Actualizar la imagen después de 10 ms

# Crear una etiqueta para mostrar la cámara
label_camera = tk.Label(root)
label_camera.pack()

# Función para mostrar el conteo del display en la ventana
def show_count(count):
    label_count.config(text="Conteo: " + str(count))  # Actualizar el texto del conteo

# Crear una etiqueta para mostrar el conteo del display
label_count = tk.Label(root, text="Conteo: ")
label_count.pack()

# Mostrar la cámara y el conteo en la ventana
show_camera()

root.mainloop()


# Cerrar la conexión serial al salir
arduino.close()
