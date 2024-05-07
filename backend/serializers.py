from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import *



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )
        return user
        



class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid password')
            else:
                raise serializers.ValidationError('User not found')

        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs
    



class BarangSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barang
        fields = ['id', 'nama_barang', 'stok', 'jumlah_terjual', 'jenis_barang']


class TransaksiSerializer(serializers.ModelSerializer):

    tanggal_transaksi = serializers.SerializerMethodField()

    def get_tanggal_transaksi(self, obj):
        created_at = obj.created_at 
        formatted_tanggal_transaksi = created_at.strftime('%d-%m-%Y')

        return formatted_tanggal_transaksi

    class Meta:
        model = Transaksi
        fields = ['id', 'tanggal_transaksi', 'barang', 'jenis_transaksi', 'jumlah']