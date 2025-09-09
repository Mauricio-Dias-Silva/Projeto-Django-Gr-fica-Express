# payments/management/commands/seed_payments.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import date, timedelta

from products.models import Product
from partners.models import Partner  # seu app de parceiros
from orders.models import QuotationRequest, Quotation

class Command(BaseCommand):
    help = 'Cria dados de teste para pagamentos'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando criação de dados de teste para pagamentos...")

        # 1️⃣ Criar parceiro de teste
        partner, created = Partner.objects.get_or_create(
            user__username='partner_test',  # supondo que Partner tem FK para CustomUser
            defaults={
                'user': Partner.user.field.related_model.objects.create_user(
                    username='partner_test',
                    email='partner_test@example.com',
                    password='test1234'
                ),
                'company_name': 'Gráfica Teste'
            }
        )
        if created:
            self.stdout.write("Parceiro de teste criado: partner_test")
        else:
            self.stdout.write("Parceiro de teste já existia: partner_test")

        # 2️⃣ Pegar ou criar um produto de teste
        product, _ = Product.objects.get_or_create(
            name='Produto Teste',
            defaults={'price': Decimal('100.00')}
        )

        # 3️⃣ Criar QuotationRequest
        quotation_request = QuotationRequest.objects.create(
            user=partner.user,  # FK para CustomUser
            product=product,
            quantity=10,
            specifications='Solicitação de teste',
            deadline=date.today() + timedelta(days=7)
        )
        self.stdout.write(f"QuotationRequest criada: #{quotation_request.id}")

        # 4️⃣ Criar Quotation
        quotation = Quotation.objects.create(
            quotation_request=quotation_request,
            partner=partner.user,
            price=Decimal('500.00'),
            production_time=5,
            notes='Orçamento de teste'
        )
        self.stdout.write(f"Quotation criada: #{quotation.id} - R${quotation.price}")
