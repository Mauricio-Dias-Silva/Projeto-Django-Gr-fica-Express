from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    # Lógica de integração com Mercado Pago
    
    return render(request, 'payments/process.html', {'order': order})

@login_required
def payment_completed(request):
    return render(request, 'payments/completed.html')

@login_required
def payment_canceled(request):
    return render(request, 'payments/canceled.html')

def mercadopago_webhook(request):
    # Processar webhook do Mercado Pago
    return HttpResponse(status=200)