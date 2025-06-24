from django.contrib import admin

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet
from panchoneta.models import *
# Register your models here.

admin.site.register(Sucursal)
admin.site.register(DetalleVenta)
admin.site.register(DetallePancho)
admin.site.register(Salsa)
admin.site.register(Bebida)

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 0

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
    list_display = ('fecha', 'sucursal') 

    ordering = ['fecha']
    search_fields = ['nombre']
    list_filter = ['sucursal']

@admin.register(Pancho)
class PanchoAdmin(admin.ModelAdmin):
    inlines = [DetallePanchoInline]
    list_display = ('nombre', 'precio')
    search_fields = ['nombre']

