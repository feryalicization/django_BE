import django_filters
from .models import *


class BarangFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name='nama_barang', lookup_expr='icontains', label='Search')

    class Meta:
        model = Barang
        fields = ['search']


class TransaksiFilter(django_filters.FilterSet):
    barang_id = django_filters.NumberFilter(field_name='barang__id', label='Barang ID')
    search = django_filters.CharFilter(field_name='jenis_transaksi', lookup_expr='icontains', label='Search')

    class Meta:
        model = Transaksi
        fields = ['barang_id', 'search']
