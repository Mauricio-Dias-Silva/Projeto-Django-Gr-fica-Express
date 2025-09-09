from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from orders.models import Order

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('approved', 'Aprovado'),
        ('authorized', 'Autorizado'),
        ('in_process', 'Em Processo'),
        ('in_mediation', 'Em Mediação'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Reembolsado'),
        ('charged_back', 'Estornado'),
    )
    
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    mercadopago_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = models.CharField(max_length=50, blank=True)
    installments = models.IntegerField(default=1)
    installments_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Transação #{self.id} - Pedido #{self.order.id} - {self.status}"
    
    def is_paid(self):
        return self.status in ['approved', 'authorized']

class Payout(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('failed', 'Falhou'),
        ('cancelled', 'Cancelado'),
    )
    
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='payouts'
    )
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='payouts'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    mercadopago_payout_id = models.CharField(max_length=100, blank=True)
    commission_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=Decimal('15.00'),
        help_text="Percentual de comissão da plataforma"
    )
    commission_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Repasse'
        verbose_name_plural = 'Repasses'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Repasse para {self.partner.partner.company_name} - Pedido #{self.order.id}"
    
    def save(self, *args, **kwargs):
        if not self.commission_amount:
            self.commission_amount = (self.amount * self.commission_percentage) / Decimal('100.00')
        super().save(*args, **kwargs)
    
    def net_amount(self):
        return self.amount - self.commission_amount

class PaymentWebhookLog(models.Model):
    mercadopago_id = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_errors = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Webhook'
        verbose_name_plural = 'Logs de Webhooks'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Webhook {self.event_type} - {self.mercadopago_id}"
