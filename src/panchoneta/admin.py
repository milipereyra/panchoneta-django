from django.contrib import admin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from panchoneta.models import *
# Register your models here.

admin.site.register(Sucursal)
admin.site.register(DetallePancho)
admin.site.register(Salsa)


@admin.register(Bebida)
class BebidaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio']
    search_fields = ['nombre']

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ('pancho', 'cantidad', 'bebida','cantidadBebida', 'venta')
    readonly_fields = ['subtotal']
    def subtotal(self, obj):
        return obj.subtotal
    subtotal.short_description = 'subtotal Detalle'

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0
    readonly_fields = ['subtotal']
    fields=('pancho','cantidad','bebida','cantidadBebida','subtotal')
    

class DetallePanchoInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        total_forms = len([form for form in self.forms if not form.cleaned_data.get('DELETE', False)])
        if total_forms > 3:
            raise ValidationError('No puede asignar más de 3 salsas a un pancho.')
    
    

class DetallePanchoInline(admin.TabularInline):
    model = DetallePancho
    extra = 0
    max_num = 3
    formset=DetallePanchoInlineFormset

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    inlines = [
        DetalleVentaInline
    ]
    list_display = ('fecha', 'sucursal','total') 
    
    ordering = ['fecha']
    search_fields = ['nombre']
    list_filter = ['sucursal']

    def total(self, obj):
        return obj.calcular_total()
    total.short_description = 'Total Venta'

@admin.register(Pancho)
class PanchoAdmin(admin.ModelAdmin):
    inlines = [DetallePanchoInline]
    list_display = ('nombre', 'precio')
    search_fields = ['nombre']

