from pymongo import MongoClient
import gridfs
from PIL import Image
import io

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mi_base_de_datos']  # Reemplaza con el nombre de tu base de datos

# Crear un objeto GridFS
fs = gridfs.GridFS(db)

# Nombre del archivo que deseas recuperar
filename = 'imagen.jpg'

# Recuperar el archivo por su filename
file_data = fs.find_one({'filename': filename})

if file_data:
    # Leer los datos del archivo
    image_data = file_data.read()

    # Convertir los datos a una imagen usando PIL
    image = Image.open(io.BytesIO(image_data))

    # Mostrar la imagen
    image.show()
else:
    print(f"No se encontró el archivo con el nombre: {filename}")
