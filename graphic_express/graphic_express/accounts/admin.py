from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomerProfile, PartnerProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'created_at')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'created_at')
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'phone', 'email_verified')
        }),
    )

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'city', 'state')
    list_filter = ('state', 'city')
    search_fields = ('user__username', 'company_name', 'cpf_cnpj')

@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'cnpj', 'specialization', 'is_approved', 'city')
    list_filter = ('specialization', 'is_approved', 'state', 'city')
    search_fields = ('user__username', 'company_name', 'cnpj')