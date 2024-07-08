from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework.exceptions import AuthenticationFailed
from simple_history.models import HistoricalRecords
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.manage import UserManager
import base64
from io import BytesIO
from PIL import Image
import os
import cv2
import numpy as np

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Usuario', max_length=255, unique=True)
    email = models.EmailField('Correo Electronico', max_length=255, unique=True)
    password = models.CharField('Password', max_length=255, null=False, blank=False)
    name = models.CharField('Nombre de Usuario', max_length=255, blank=True, null=True)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    profession = models.CharField('Profesion', max_length=255, blank=True, null=True, default='Estudiante')
    image_face = models.TextField('ImageFace', blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    historical = HistoricalRecords()
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        db_table = 'users'

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username', 'name', 'last_name']

    def tokens(self):    
        refresh = RefreshToken.for_user(self)
        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

    def __str__(self):
        return self.email
    
    @property
    def get_full_name(self):
        return f"{self.name.title()} {self.last_name.title()}"
    
    def extract_base64_data(self, image_base64):
        # Extraer la parte codificada en base64 de la cadena
        try:
            data_extract = image_base64.split(',')[1] #Extrae la imagen en base64
            return base64.b64decode(data_extract) #Decodificar la cadena BASE64 en bytes y la retornamos
        except Exception as e:
            raise ValueError(f"Formato de imagen base64 no válido: {str(e)}")

    def create_imageJPEG(self, image_bytes, url):
        try:
            image = Image.open(BytesIO(image_bytes))
            image.save(url)
        except Exception as e:
            raise ValueError(f"Error en la creacion de imagen: {str(e)}")
        
    def destroy_imageJPEG(self, url):
        try:
            os.remove(url)
        except Exception as e:
            raise ValueError(f"Error en la eliminacion de la imagen: {str(e)}")

    def extract_features(self, image):
    # Calcula el valor promedio de los canales de color (R, G, B)
        b, g, r = cv2.split(image)
        avg_b = b.mean()
        avg_g = g.mean()
        avg_r = r.mean()
        return [avg_b, avg_g, avg_r]

    def calculate_distance(self, feature1, feature2):
        # Calcula la distancia euclidiana entre los vectores de características
        feature1 = np.array(feature1)
        feature2 = np.array(feature2)
        return np.linalg.norm(feature1 - feature2)

    def recognition_face(self, url_known, url_unknown):
        print(f"known: {url_known}")
        print(f"unknown: {url_unknown}")
        #Carga de imagenes
        try:
            known_image = cv2.imread(url_known)
            unknown_image = cv2.imread(url_unknown)
            
            known_feature = self.extract_features(known_image)  
            unknown_feature = self.extract_features(unknown_image)
            # Comparar características (por ejemplo, usando distancia euclidiana)
            distance = self.calculate_distance(known_feature, unknown_feature)
        except Exception as e:
            raise ValueError(f"Error en el tratamiento de imagenes: {str(e)}")
        
        if round(100 - distance,2) > 75:
            os.remove(url_unknown)
            return f"data:image/jpeg;base64,{self.image_face}"
        else:
            raise AuthenticationFailed("La imagen no coincide con tu imagen de registro")
