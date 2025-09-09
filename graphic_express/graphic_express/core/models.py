from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default='Gráfica Express')
    site_description = models.TextField(
        default='Conectando clientes às melhores gráficas'
    )
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('15.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Percentual padrão de comissão"
    )
    default_production_days = models.IntegerField(
        default=3,
        help_text="Dias úteis padrão para produção"
    )
    min_order_value = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('29.90'),
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Valor mínimo para pedidos"
    )
    contact_email = models.EmailField(default='contato@graficaexpress.com.br')
    contact_phone = models.CharField(max_length=15, default='(11) 99999-9999')
    is_maintenance_mode = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração do Site'
        verbose_name_plural = 'Configurações do Site'
    
    def __str__(self):
        return f"Configurações do {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Garante que só existe uma configuração
        self.__class__.objects.exclude(id=self.id).delete()
        super().save(*args, **kwargs)

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Pergunta Frequente'
        verbose_name_plural = 'Perguntas Frequentes'
        ordering = ('order',)
    
    def __str__(self):
        return self.question

class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('new', 'Nova'),
        ('read', 'Lida'),
        ('replied', 'Respondida'),
        ('closed', 'Fechada'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='new'
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.subject} - {self.name}"