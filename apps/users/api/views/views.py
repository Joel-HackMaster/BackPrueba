from rest_framework.response import Response
from apps.users.api.serializers.serializer import UserSerializer, MyTokenObtainPairSerializer, LoginSerializer, LogoutUserSerializer
from rest_framework import status, viewsets
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthenticatedForList


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data=serializer.data
            return Response({
                'data':user_data,
                'message':'Registro Exitoso'
            }, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutApiView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TestingLogueo(GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        data={
            'msg': 'its works'
        }
        return Response(data, status=status.HTTP_200_OK)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

