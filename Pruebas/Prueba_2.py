import tkinter as tk
from PIL import Image, ImageTk
import serial
import threading
import cv2

# Configurar el puerto serial
ser = serial.Serial('COM3', 9600, timeout=1)  # Cambiar 'COM3' al puerto correcto

# Crear una ventana tkinter
window = tk.Tk()
window.title("Cámara")

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Variable global para el factor de zoom
zoom_factor = 1.0

# Variable global para mantener el contador de fotos
contador_fotos = 0

# Variable para el conteo del display
conteo_display = ""

def leer_serial():
    global zoom_factor, contador_fotos, conteo_display
    while True:
        # Leer datos del puerto serial
        mensaje = ser.readline().decode().strip()
        if mensaje.isdigit():
            # Si se recibe un valor numérico, actualizar el conteo del display
            conteo_display = mensaje
        elif mensaje.startswith("Zoom"):
            # Si se recibe un valor numérico con prefijo Zoom, actualizar el factor de zoom
            valor_zoom = mensaje.split(" ")[1]
            if valor_zoom.isdigit():
                zoom_factor = 1.0 + int(valor_zoom) / 1000.0
        elif mensaje == "Boton presionado":
            # Si se recibe el mensaje "Boton presionado", tomar una foto y guardarla
            tomar_foto()
            contador_fotos += 1

# Función para tomar una foto y guardarla
def tomar_foto():
    global contador_fotos
    # Capturar una imagen
    ret, frame = cap.read()
    if ret:
        # Guardar la imagen con un nombre único
        filename = f"imagen_{contador_fotos}.png"
        cv2.imwrite(filename, frame)
        print(f"Foto guardada como {filename}")

# Función para enviar el comando de inicio de conteo al Arduino
def send_command():
    ser.write(b'C')  # Enviar el comando para iniciar el conteo
    print("Comando enviado")

# Crear un hilo para leer mensajes del puerto serial
thread_serial = threading.Thread(target=leer_serial)
thread_serial.daemon = True
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
        
        # Actualizar la etiqueta del conteo
        label_conteo.config(text=f"Conteo: {conteo_display}")

# Crear un panel en la ventana para mostrar la imagen de la cámara
panel = tk.Label(window)
panel.pack()

# Crear una etiqueta para mostrar el conteo del display
label_conteo = tk.Label(window, text="Conteo: ", font=("Helvetica", 16))
label_conteo.pack(pady=10)

# Crear un botón para iniciar el conteo
button = tk.Button(window, text="Iniciar Conteo", command=send_command)
button.pack(pady=10)

# Iniciar el proceso de mostrar la imagen de la cámara
mostrar_camara()

# Ajustar el tamaño de la ventana para que coincida con el tamaño de la cámara
window.geometry(f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

# Iniciar el bucle principal de tkinter
window.mainloop()

# Cerrar la conexión serial al salir
ser.close()
