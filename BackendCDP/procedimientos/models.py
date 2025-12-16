from django.db import models
from django.conf import settings
from pacientes.models import Paciente


class Arancel(models.Model):
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=100)

    # Auditoría
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='arancel_created')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='arancel_updated')
    deleted_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='arancel_deleted')

    def __str__(self):
        return self.descripcion


class Factura(models.Model):
    id_paciente = models.ForeignKey(Paciente,on_delete=models.CASCADE,related_name="facturas")
    fecha = models.DateField()
    total = models.DecimalField(max_digits=12, decimal_places=2)

    # Auditoría
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='factura_created')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='factura_updated')
    deleted_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='factura_deleted')

    def __str__(self):
        return f"Factura #{self.id} - Paciente: {self.id_paciente.nombre}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura,on_delete=models.CASCADE,related_name="detalles")
    id_arancel = models.ForeignKey(Arancel,on_delete=models.SET_NULL,null=True,related_name="detalles")

    # En tu diagrama: se guardan estos campos de forma "copiada"
    arancel_descripcion = models.CharField(max_length=255)
    arancel_tipo = models.CharField(max_length=100)
    arancel_precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Auditoría
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='detallefactura_created')
    update_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,related_name='detallefactura_updated')
    deleted_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name='detallefactura_deleted')

    def __str__(self):
        return f"Detalle #{self.id} de Factura #{self.factura.id}"

