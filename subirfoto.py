from pymongo import MongoClient
import gridfs

# Conectar a la base de datos MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mi_base_de_datos']  # Reemplaza con el nombre de tu base de datos

# Crear un objeto GridFS
fs = gridfs.GridFS(db)

# Ruta a la imagen que deseas subir
image_path = 'i792159.jpeg'

# Abrir la imagen en modo binario y guardarla en MongoDB
with open(image_path, 'rb') as f:
    contents = f.read()
    file_id = fs.put(contents, filename='imagen.jpg')  # Puedes añadir más metadatos si lo deseas

print(f'Imagen subida con ID: {file_id}')
