from django.db import models



class Barang(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    nama_barang = models.CharField(max_length=255, null=True, blank=True)
    stok = models.IntegerField(default=0, null=True, blank=True)
    jumlah_terjual = models.IntegerField(default=0, null=True, blank=True)
    jenis_barang = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.nama_barang or 'Barang Tidak Ada'
    

class Transaksi(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    barang = models.ForeignKey(
        Barang, on_delete=models.CASCADE, related_name='barangs')
    jumlah = models.IntegerField(default=0, null=True, blank=True)
    jenis_transaksi = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return f"Transaksi {self.id}"
    