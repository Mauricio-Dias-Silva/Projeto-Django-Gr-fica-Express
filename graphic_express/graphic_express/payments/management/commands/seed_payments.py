
from partners.models import Partner
from orders.models import QuotationRequest, Quotation
from django.core.management.base import BaseCommand
from decimal import Decimal

from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria dados de teste para pagamentos de teste'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando criação de dados de teste para pagamentos...")

        # Cria usuário Django
        user, _ = User.objects.get_or_create(
            username='partner_test',
             defaults={'email': 'partner_test@example.com', 'password': 'test1234'}
        )

        # Cria parceiro vinculado
        partner, created = Partner.objects.get_or_create(
            user=user,
            defaults={'company_name': 'Parceiro Teste', 'cnpj': '00.000.000/0001-00'}
        )

        # Cria requisição de cotação
        quotation_request = QuotationRequest.objects.create(
            partner=partner,
            description='Solicitação de teste'
        )

        # Cria cotação vinculada à requisição
        quotation = Quotation.objects.create(
            partner=partner,
            quotation_request=quotation_request,
            price=Decimal('200.00'),
            notes='Cotação de teste',
            production_time=5
        )

        self.stdout.write("Dados de teste criados com sucesso!")
