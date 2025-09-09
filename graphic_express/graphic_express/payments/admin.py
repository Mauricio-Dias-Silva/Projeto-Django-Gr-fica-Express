from django.contrib import admin
from .models import Transaction, Payout, PaymentWebhookLog

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id', 'mercadopago_id')

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('partner', 'order', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('partner__username', 'order__id')

@admin.register(PaymentWebhookLog)
class PaymentWebhookLogAdmin(admin.ModelAdmin):
    list_display = ('mercadopago_id', 'event_type', 'processed', 'created_at')
    list_filter = ('processed', 'created_at')
