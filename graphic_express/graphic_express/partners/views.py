# partners/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PartnerRegistrationForm
from .models import Partner  # <--- importando o modelo correto

def partner_register(request):
    if request.method == 'POST':
        form = PartnerRegistrationForm(request.POST)
        if form.is_valid():
            partner = form.save(commit=False)
            partner.user = request.user  # vincula o parceiro ao usuário logado
            partner.save()
            return redirect('partners:dashboard')
    else:
        form = PartnerRegistrationForm()
    
    return render(request, 'partners/partner_register.html', {'form': form})

@login_required
def partner_dashboard(request):
    # traz os dados do parceiro logado
    partner = Partner.objects.filter(user=request.user).first()
    return render(request, 'partners/dashboard.html', {'partner': partner})

@login_required
def partner_orders(request):
    partner = Partner.objects.filter(user=request.user).first()
    return render(request, 'partners/orders.html', {'partner': partner})
