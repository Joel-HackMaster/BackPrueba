from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import face_recognition
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import base64
import cv2
import numpy as np


class UserSerializer(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=72, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name', 'profession', 'password', 'image')

    def validate_email(self, value):
        if value is None:
            raise serializers.ValidationError('Tienes que indicar un correo')
        user = User.objects.filter(email = value).first()
        if user is not None:
            raise serializers.ValidationError('Ya existe un usuario con ese correo')
        return value
    
    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username = validated_data.get('username'),
                email = validated_data.get('email'),
                name = validated_data.get('name'),
                last_name = validated_data.get('last_name'),
                profession = validated_data.get('profession'),
                password = validated_data.get('password'),
                image_face = validated_data.get('image').split(',')[1],
            )
            new_user = User.objects.filter(email = validated_data.get('email')).first()
            print(f"ID: {new_user.id} Email: {new_user.email}")
            image_bytes = new_user.extract_base64_data(image_base64=validated_data.get('image'))
            new_user.create_imageJPEG(
                image_bytes=image_bytes,
                url=f"C:\\ProyectosPython\\Backends\\BackPrueba\\BackPrueba\\apps\\users\\api\\assets\\image_known\\{new_user.id}.jpeg"
            )
        except Exception as e:
            raise ValueError(e)
        return user
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'profession': instance.profession,
        }

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name= serializers.CharField(max_length=150, read_only=True)
    image= serializers.CharField(write_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)
    photo= serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'access_token', 'refresh_token', 'image', 'photo')
        

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        image = attrs.get('image')
        request=self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Usuario o contraseña incorrectos")
        
        url_unknown=f"C:\\ProyectosPython\\Backends\\BackPrueba\\BackPrueba\\apps\\users\\api\\assets\\image_unknown\\{user.id}.jpeg"
        url_known=f"C:\\ProyectosPython\\Backends\\BackPrueba\\BackPrueba\\apps\\users\\api\\assets\\image_known\\{user.id}.jpeg"
        image_bytes=user.extract_base64_data(image_base64=image)
        user.create_imageJPEG(
            image_bytes=image_bytes,
            url=url_unknown
        )
        
        image_64 = user.recognition_face(
            url_known = url_known,
            url_unknown = url_unknown
        )

        tokens = user.tokens()
        return{
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(tokens.get('access')),
            'refresh_token': str(tokens.get('refresh')),
            'photo': image_64
        }        


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages={
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
