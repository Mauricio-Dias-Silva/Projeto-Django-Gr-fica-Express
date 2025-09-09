from django.shortcuts import render
from products.models import Product

def home(request):
    # Pegar alguns produtos para exibir na página inicial
    featured_products = Product.objects.filter(available=True)[:4]
    return render(request, 'core/home.html', {'featured_products': featured_products})


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')