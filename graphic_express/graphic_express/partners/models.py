from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from products.models import Category

class Partner(models.Model):
    SPECIALIZATION_CHOICES = (
        ('digital', 'Impressão Digital'),
        ('offset', 'Impressão Offset'),
        ('large_format', 'Grande Formato'),
        ('corporate', 'Material Corporativo'),
        ('promotional', 'Material Promocional'),
        ('varied', 'Variados'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pendente de Aprovação'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('suspended', 'Suspenso'),
    )
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner'
    )
    company_name = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=18, unique=True)
    specialization = models.CharField(
        max_length=20, 
        choices=SPECIALIZATION_CHOICES,
        default='varied'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    capacity = models.IntegerField(
        default=5,
        help_text="Número máximo de pedidos simultâneos",
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    current_orders = models.IntegerField(default=0)
    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    total_ratings = models.IntegerField(default=0)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    delivery_radius_km = models.IntegerField(
        default=50,
        help_text="Raio de entrega em quilômetros",
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Gráfica Parceira'
        verbose_name_plural = 'Gráficas Parceiras'
        ordering = ('company_name',)
    
    def __str__(self):
        return f"{self.company_name} - {self.get_specialization_display()}"
    
    def has_capacity(self):
        return self.current_orders < self.capacity
    
    def available_slots(self):
        return self.capacity - self.current_orders
    
    def update_rating(self, new_rating):
        """Atualiza a avaliação média da gráfica"""
        total_score = (self.rating * self.total_ratings) + new_rating
        self.total_ratings += 1
        self.rating = total_score / self.total_ratings
        self.save()

class PartnerSpecialization(models.Model):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='specialized_partners'
    )
    expertise_level = models.IntegerField(
        default=1,
        help_text="Nível de especialização (1-5)",
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Especialização da Gráfica'
        verbose_name_plural = 'Especializações das Gráficas'
        unique_together = ('partner', 'category')
    
    def __str__(self):
        return f"{self.partner.company_name} - {self.category.name} (Nível {self.expertise_level})"

class PartnerEquipment(models.Model):
    EQUIPMENT_TYPES = (
        ('printer', 'Impressora'),
        ('cutter', 'Cortadora'),
        ('binder', 'Encadernadora'),
        ('finishing', 'Acabamento'),
        ('other', 'Outro'),
    )
    
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='equipments'
    )
    name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=20, choices=EQUIPMENT_TYPES)
    brand = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    capacity = models.CharField(max_length=100, blank=True, help_text="Capacidade de produção")
    is_operational = models.BooleanField(default=True)
    acquired_date = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Equipamento da Gráfica'
        verbose_name_plural = 'Equipamentos das Gráficas'
    
    def __str__(self):
        return f"{self.name} - {self.partner.company_name}"

class PartnerServiceArea(models.Model):
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='service_areas'
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    delivery_days = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(30)]
    )
    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    class Meta:
        verbose_name = 'Área de Serviço'
        verbose_name_plural = 'Áreas de Serviço'
        unique_together = ('partner', 'city', 'state')
    
    def __str__(self):
        return f"{self.city}/{self.state} - {self.partner.company_name}"