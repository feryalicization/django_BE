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
from .query import *
from django.db import connections





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


    def perform_create(self, serializer):
        jenis_transaksi = serializer.validated_data.get('jenis_transaksi')
        barang = serializer.validated_data.get('barang')
        jumlah = serializer.validated_data.get('jumlah')

        if jenis_transaksi == 'beli':
            barang.stok += jumlah
            barang.save(update_fields=['stok'])
            barang.jumlah_terjual += jumlah
            barang.save(update_fields=['jumlah_terjual'])
        elif jenis_transaksi == 'jual':
            if barang.stok >= jumlah:
                barang.stok -= jumlah
                barang.save(update_fields=['stok'])
                barang.jumlah_terjual += jumlah
                barang.save(update_fields=['jumlah_terjual'])
            else:
                return Response({'error': 'Insufficient stock'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TransaksiDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaksi.objects.all()
    serializer_class = TransaksiSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated] 




class Perbandingan(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ],
        responses={200: 'Success', 400: 'Bad Request', 404: 'Not Found'},
    )

    def get(self, request):
        
        serializer = PerbandinganQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')

        query = perbandingan(start_date, end_date)

        with connections['default'].cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        data = []

        for item in result:
            jenis_barang, transaksi = item  
            data.append({
                'jenis_barang': jenis_barang,
                'transaksi': transaksi
            })

        return Response(data)