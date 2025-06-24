from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import DetalleVenta, Venta

def actualizar_total_venta(venta):
    total = 0
    for detalle in venta.detalleventa_set.all():
        total += detalle.subtotal or 0
    venta.total = total
    venta.save()

@receiver(post_save, sender=DetalleVenta)
def actualizar_total_venta_al_guardar(sender, instance, **kwargs):
    if instance.venta:
        actualizar_total_venta(instance.venta)

@receiver(post_delete, sender=DetalleVenta)
def actualizar_total_venta_al_eliminar(sender, instance, **kwargs):
    if instance.venta:
        actualizar_total_venta(instance.venta)