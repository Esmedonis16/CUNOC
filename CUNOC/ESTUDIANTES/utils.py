import face_recognition as fr
import numpy as np
from profiles.models import Profile


def is_ajax(request):
    return request.headers.get('x-request-with') == 'XMLHttpRequest'


def get_encoded_faces():
    """
    Esta funcion carga todas las imagenes de perfil de los usuarios
    y codifica sus rostros
    """
    #obtener todos los perfiles de usuarios desde la base de datos
    qs = Profile.objects.all()
    
    #crear un diccionario para guardar la cara codificada de cada ususario
    encoded = {}
    
    for p in qs:
        #iniciando la variable de codificacion como None
        encoding = None
        
        #Obteniendo la imagen de perfil del usuario
        face = fr.load_image_file(p.photo.path)
        
        #codifica el restro si lo detecta
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print('Rostro no encontrado en la imagen')
            
        #Agregar el rostro codificado al diccionario si encoding no es None
        if encoding is not  None:
            encoded[p.user.username] = encoding
            
    #Agregar retunr del diccionario con los rostros codificados
    return encoded


def classiffy_face(img):
    """
    Esta funcion toma una imagen como input y regresa el nombre del rostro si existe uno
    """
    #Cargando todas las caras conocidas y su codificaciones
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    know_face_names = list(faces.keys())
    
    #Cargando la imagen de input
    img = fr.load_image_file(img)
    
    try:
        #Encontrando todos los rsotros en la imagen input
        face_locations = fr.face_locations(img)
        
        #Codificar los rostros en la imagen Input
        unknow_face_encodings = fr.face_encodings(img, face_locations)
        
        #Identificar los rostros de la imagen input
        face_names =[]
        for face_encoding in unknow_face_encodings:
            #Comparar la codificacion de la cara actual con las codificaciones de todas
            matches = fr.compare_faces(faces_encoded, face_encoding)
            
            #Encuentra la cara conocida con la codificacion mas cercana a la cara actual
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            #Si la cara conocida mas cercana coincide con la cara actual, etiqueta la cara
            if matches[best_match_index]:
                name = know_face_names[best_match_index]
            else:
                name = "Desconocido"
            
            face_names.append(name)
            
        #Devolver el nombre de la primera cara de la imagen de entrada
        return face_names[0]
    except:
        #Si no se encuentran caras en la imagen de entrada o se produce un error, devuelve
        return False  