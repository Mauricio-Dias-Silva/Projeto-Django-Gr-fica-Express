# partners/admin.py
from django.contrib import admin
from .models import Partner, PartnerEquipment, PartnerServiceArea, PartnerSpecialization

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'cnpj', 'specialization', 'capacity', 'status', 'city', 'state')
    list_filter = ('specialization', 'status', 'city', 'state')
    search_fields = ('company_name', 'cnpj')

@admin.register(PartnerEquipment)
class PartnerEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'partner', 'equipment_type', 'brand', 'model', 'is_operational')

@admin.register(PartnerServiceArea)
class PartnerServiceAreaAdmin(admin.ModelAdmin):
    list_display = ('partner', 'city', 'state', 'delivery_days', 'delivery_cost')

@admin.register(PartnerSpecialization)
class PartnerSpecializationAdmin(admin.ModelAdmin):
    list_display = ('partner', 'category', 'expertise_level')
