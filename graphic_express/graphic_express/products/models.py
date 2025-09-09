from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(
        Category, 
        related_name='products', 
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    specifications = models.TextField(
        blank=True, 
        help_text="Especificações técnicas do produto"
    )
    base_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    available = models.BooleanField(default=True)
    min_quantity = models.IntegerField(default=1)
    max_quantity = models.IntegerField(default=10000)
    production_days = models.IntegerField(
        default=3,
        help_text="Dias úteis para produção"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])
    
    def calculate_price(self, quantity):
        """Calcula o preço baseado na quantidade"""
        from .utils import calculate_product_price  # Importação local para evitar circular imports
        return calculate_product_price(self, quantity)

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    description = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
    
    def __str__(self):
        return f"Imagem de {self.product.name}"

class PriceRule(models.Model):
    product = models.ForeignKey(
        Product, 
        related_name='price_rules', 
        on_delete=models.CASCADE
    )
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField(
        blank=True, 
        null=True,
        help_text="Deixe em branco para quantidade ilimitada"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Regra de Preço'
        verbose_name_plural = 'Regras de Preço'
        ordering = ('min_quantity',)
        unique_together = ('product', 'min_quantity')
    
    def __str__(self):
        max_qty = self.max_quantity if self.max_quantity else '+'
        return f"{self.product.name} - {self.min_quantity}-{max_qty}: R${self.price}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.max_quantity and self.max_quantity <= self.min_quantity:
            raise ValidationError('A quantidade máxima deve ser maior que a mínima.')