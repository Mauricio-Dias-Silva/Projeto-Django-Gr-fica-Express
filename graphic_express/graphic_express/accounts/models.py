from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Cliente'),
        ('partner', 'Gráfica Parceira'),
        ('admin', 'Administrador'),
    )
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='customer'
    )
    phone = models.CharField(max_length=15, blank=True)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_customer(self):
        return self.user_type == 'customer'
    
    def is_partner(self):
        return self.user_type == 'partner'
    
    def is_admin(self):
        return self.user_type == 'admin'

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    company_name = models.CharField(max_length=100, blank=True)
    cpf_cnpj = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=2, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = 'Perfil do Cliente'
        verbose_name_plural = 'Perfis dos Clientes'
    
    def __str__(self):
        return f"Cliente: {self.user.username}"
    


class PartnerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20)
    specialization = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.company_name

