import tkinter as tk
import cv2
from PIL import Image, ImageTk
import serial

class WebcamApp:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        
        self.vid = cv2.VideoCapture(video_source)
        
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        self.btn_snapshot = tk.Button(window, text="Tomar foto", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
        
        self.ser = serial.Serial('COM3', 9600)  # Cambia 'COM3' al puerto que esté utilizando tu Arduino
        
        self.update()
        
        self.window.mainloop()
        
    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            zoom_value = int(self.ser.readline().strip())  # Lee el valor del potenciómetro desde Arduino
            # Utiliza el valor del potenciómetro para ajustar el zoom de la cámara (código no implementado)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

# Cambia 0 a otro número si tu cámara no está en el primer índice.
WebcamApp(tk.Tk(), "Webcam App")