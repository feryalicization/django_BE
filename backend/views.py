from rest_framework import generics
from .models import *
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
import requests
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.views import APIView
from django.conf import settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .filters import *



class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': f'Token {token.key}'
        })




class BarangListCreateAPIView(generics.ListCreateAPIView):
    queryset = Barang.objects.all()
    serializer_class = BarangSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BarangFilter
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]  


class BarangDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Barang.objects.all()
    serializer_class = BarangSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 

class TransaksiListCreateAPIView(generics.ListCreateAPIView):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransaksiFilter
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]  


class TransaksiDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 
