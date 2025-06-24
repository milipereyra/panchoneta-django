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
    
        
class Venta(NombreAbstract):
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

    class Meta:
        verbose_name = 'venta'
        verbose_name_plural = 'ventas'

class DetalleVenta(NombreAbstract):
    cantidad = models.BigIntegerField(_('cantidad'),
        help_text=_('cantidad panchos'),
        blank=True,
        null=True
    )
    subtotal = models.DecimalField(_('subtotal'),
        help_text=_('subtotal del detalleventa'),
        max_digits=10,
        decimal_places=2,
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
    pancho = models.ForeignKey(
        Pancho,
        help_text=_('bebida encargadas'),
        related_name='%(app_label)s_%(class)s_related',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    venta = models.ForeignKey(Venta, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'detalleventa'
        verbose_name_plural = 'detalles'

class DetallePancho(NombreAbstract):
    #idSalsaxPancho, idSalsa, idPancho
    idSalsa=models.ForeignKey(Salsa, help_text=_('salsa'), related_name='%(app_label)s_%(class)s_related',on_delete=models.PROTECT, blank=False,null=False)
    idPancho=models.ForeignKey(Pancho, help_text=_('pancho'), related_name='%(app_label)s_%(class)s_related',on_delete=models.PROTECT, blank=False,null=False)