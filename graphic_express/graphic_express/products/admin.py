from django.contrib import admin
from .models import Category, Product, ProductImage, PriceRule

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class PriceRuleInline(admin.TabularInline):
    model = PriceRule
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'available')
    list_filter = ('category', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, PriceRuleInline]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')
    list_filter = ('is_main',)

@admin.register(PriceRule)
class PriceRuleAdmin(admin.ModelAdmin):
    list_display = ('product', 'min_quantity', 'max_quantity', 'price')
    list_filter = ('product',)