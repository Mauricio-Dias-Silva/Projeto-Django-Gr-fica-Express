from django.contrib import admin
from .models import QuotationRequest, Quotation, Order, OrderTracking, Review

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'quotation__partner__partner__company_name', 'tracking_code')

@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__id',)

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('id', 'quotation_request', 'partner', 'price', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')
    search_fields = ('partner__partner__company_name', 'quotation_request__product__name')

@admin.register(QuotationRequest)
class QuotationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'product__name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'rating', 'would_recommend', 'created_at')
    list_filter = ('rating', 'would_recommend', 'created_at')
    search_fields = ('order__id', 'order__user__username')
