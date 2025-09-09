from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from products.models import Product

class QuotationRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('sent_to_partners', 'Enviado para Gráficas'),
        ('processing', 'Processando'),
        ('completed', 'Concluído'),
        ('canceled', 'Cancelado'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='quotation_requests'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='quotation_requests'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    specifications = models.TextField(
        blank=True,
        help_text="Especificações adicionais do pedido"
    )
    deadline = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Solicitação de Orçamento'
        verbose_name_plural = 'Solicitações de Orçamento'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Orçamento #{self.id} - {self.product.name}"
    
    def total_quotations(self):
        return self.quotations.count()
    
    def best_quotation(self):
        return self.quotations.order_by('price').first()

class Quotation(models.Model):
    quotation_request = models.ForeignKey(
        QuotationRequest, 
        related_name='quotations', 
        on_delete=models.CASCADE
    )
    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='quotations'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    notes = models.TextField(
        blank=True,
        help_text="Observações da gráfica sobre o orçamento"
    )
    production_time = models.IntegerField(
        help_text="Tempo de produção em dias úteis"
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ('price',)
        unique_together = ('quotation_request', 'partner')
    
    def __str__(self):
        return f"Orçamento #{self.id} - {self.partner.partner.company_name}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('in_production', 'Em Produção'),
        ('quality_check', 'Controle de Qualidade'),
        ('ready', 'Pronto para Entrega'),
        ('in_transit', 'Em Trânsito'),
        ('delivered', 'Entregue'),
        ('canceled', 'Cancelado'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quotation = models.OneToOneField(
        Quotation, 
        on_delete=models.CASCADE,
        related_name='order'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    tracking_code = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.total_price and self.quotation:
            self.total_price = self.quotation.price
        super().save(*args, **kwargs)

class OrderTracking(models.Model):
    order = models.ForeignKey(
        Order, 
        related_name='tracking_entries', 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20, 
        choices=Order.STATUS_CHOICES
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Rastreamento de Pedido'
        verbose_name_plural = 'Rastreamentos de Pedidos'
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"Tracking #{self.id} - {self.order}"

class Review(models.Model):
    RATING_CHOICES = (
        (1, '⭐ - Muito Ruim'),
        (2, '⭐⭐ - Ruim'),
        (3, '⭐⭐⭐ - Regular'),
        (4, '⭐⭐⭐⭐ - Bom'),
        (5, '⭐⭐⭐⭐⭐ - Excelente'),
    )
    
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE,
        related_name='review'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    would_recommend = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
    
    def __str__(self):
        return f"Avaliação {self.rating}★ para Pedido #{self.order.id}"