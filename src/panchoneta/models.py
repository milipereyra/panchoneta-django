from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

#clase herencia/interfaz
class NombreAbstract(models.Model):
    nombre = models.CharField(
        _('Nombre'),
        help_text=_('Nombre descriptivo'),
        max_length=200,
        # unique=True,
    )

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.nombre}'

    class Meta:
        abstract = True
        ordering = ['nombre']

class BaseModel(models.Model):
    class Meta:
        abstract = True

class Bebida(NombreAbstract):
    nombre = models.TextField(_('nombre'), 
            help_text=_('nombre de la bebida'),
            blank=True,
            null=True
        )
    precio = models.DecimalField( _('precio'),
            help_text=_('Precio de la bebida'),
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True
        )

class Pancho(NombreAbstract):
    #idPancho, nombre, precio
    nombre = models.TextField(_('nombre'),
                              help_text=_('nombre del pancho'),
                              blank=False,
                              null=False
                            )
    
    precio = models.DecimalField(_('precio'),
                                    max_digits=15,
                                    decimal_places=2,
                                    help_text=_('precio del pancho expresado en pesos'),
                                    default=0
                                )
    class Meta:
        verbose_name= 'pancho'
        verbose_name_plural = 'panchos'

class Salsa(NombreAbstract):
    
    #idSalsa, nombreSalsa, descripcion
    nombre = models.TextField(_('nombre'),
                                   help_text=_('nombre de la salsa'),
                                   blank = True,
                                   null=True
                                )
    
    descripcion = models.TextField(_('descripcion'),
                                   help_text=_('descripcion de la salsa'),
                                   blank=True,
                                   null=True)
    
    class Meta:
        verbose_name='salsa',
        verbose_name_plural='salsas'
    
    
class Sucursal(NombreAbstract):
    #nombre, calle, nroCalle, piso
    nombre = models.TextField(_('nombre'), 
                                help_text=_('nombre de la sucursal'),
                                blank=True,
                                null=True
                            )
    
    calle = models.TextField(_('calle'), 
                             help_text=_('calle de la sucursal'),
                             blank=True,
                             null=True
                             )
    
    nroCalle = models.BigIntegerField(_('nroCalle'),
                                      help_text=_('nro. de la calle'),
                                      blank=True,
                                      null=True
                            )
    
    piso = models.BigIntegerField(_('piso'),
                                  help_text=_('nro. de piso'),
                                  blank=True,
                                  null=True
                                 )
    
        
class Venta(models.Model):
    #atributos
    fecha = models.DateField(_('fecha'),
                            help_text=_('fecha de la venta'),
                            blank=True,
                            null=True
                            )    
    hora = models.TimeField(_('hora'),
                            help_text= _('hora de la venta'),
                            blank=True,
                            null=True
                            )


    #relaciones
    sucursal=models.ForeignKey(Sucursal, help_text=_('sucursal'), related_name='%(app_label)s_%(class)s_related',on_delete=models.PROTECT, blank=False,null=False)

    def __str__(self):
        return f"Venta #{self.pk} - {self.fecha} - {self.sucursal.nombre if self.sucursal else ''}"

    def calcular_total(self):
        total = 0
        for detalle in self.detalleventa_set.all():
            if detalle.subtotal is None:
                detalle.subtotal = detalle.calcular_subtotal()
                detalle.save()
            total += detalle.subtotal
        return total
    
    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

class DetalleVenta(models.Model):
    pancho = models.ForeignKey(
        Pancho,
        help_text=_('bebida encargadas'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    cantidad = models.BigIntegerField(_('cantidad'),
        help_text=_('cantidad panchos'),
        blank=True,
        null=True
    )
    
    bebida= models.ForeignKey(
        Bebida,
        help_text=_('bebida encargadas'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    cantidadBebida = models.BigIntegerField(_('cantidad bebida'),
        help_text=_('cantidad bebidas'),
        blank=True,
        null=True
    )

    
    @property
    def subtotal(self):
        precio_pancho = self.pancho.precio if self.pancho else 0
        precio_bebida = self.bebida.precio if self.bebida else 0
        cantidad = self.cantidad or 0
        cantidadBebida = self.cantidadBebida or 0
        return (precio_pancho * cantidad) + (precio_bebida * cantidadBebida)
    
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        pancho_nombre = self.pancho.nombre if self.pancho else "Sin pancho"
        bebida_nombre = self.bebida.nombre if self.bebida else "Sin bebida"
        return f"{pancho_nombre} x{self.cantidad or 0} + {bebida_nombre}x{self.cantidadBebida or 0}"

    class Meta:
        verbose_name = 'detalleventa'
        verbose_name_plural = 'detallesVenta'

class DetallePancho(models.Model):
    #idSalsaxPancho, idSalsa, idPancho
    idSalsa=models.ForeignKey(Salsa, help_text=_('salsa'), related_name='%(app_label)s_%(class)s_related',on_delete=models.PROTECT, blank=False,null=False)
    idPancho=models.ForeignKey(Pancho, help_text=_('pancho'), related_name='%(app_label)s_%(class)s_related',on_delete=models.PROTECT, blank=False,null=False)