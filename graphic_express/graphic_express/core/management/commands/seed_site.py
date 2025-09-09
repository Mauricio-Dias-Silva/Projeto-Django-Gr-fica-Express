from django.core.management.base import BaseCommand
from core.models import SiteConfiguration, FAQ, ContactMessage  # ajuste 'your_app'

class Command(BaseCommand):
    help = 'Popula dados iniciais de configuração, FAQs e mensagens de contato'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando criação de dados de teste para site...")

        # ---------- Site Configuration ----------
        site_config = SiteConfiguration(
            site_name="Gráfica Express",
            site_description="Conectando clientes às melhores gráficas",
            commission_percentage=15.00,
            default_production_days=3,
            min_order_value=29.90,
            contact_email="contato@graficaexpress.com.br",
            contact_phone="(11) 99999-9999",
            is_maintenance_mode=False
        )
        site_config.save()
        self.stdout.write(self.style.SUCCESS("SiteConfiguration criada com sucesso!"))

        # ---------- FAQs ----------
        faqs = [
            {"question": "Como faço um pedido?", "answer": "Selecione o produto, configure e finalize o pedido no carrinho.", "order": 1},
            {"question": "Qual o prazo de produção?", "answer": "O prazo padrão é de 3 dias úteis, podendo variar conforme o produto.", "order": 2},
            {"question": "Quais formas de pagamento?", "answer": "Aceitamos cartão de crédito, Pix e boleto bancário.", "order": 3},
        ]

        for faq_data in faqs:
            faq, created = FAQ.objects.get_or_create(**faq_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"FAQ criada: {faq.question}"))
            else:
                self.stdout.write(self.style.WARNING(f"FAQ já existia: {faq.question}"))

        # ---------- Contact Messages ----------
        messages = [
            {"name": "João Silva", "email": "joao@email.com", "subject": "Orçamento rápido", "message": "Gostaria de um orçamento para 100 cartões de visita.", "status": "new"},
            {"name": "Maria Souza", "email": "maria@email.com", "subject": "Dúvida sobre prazo", "message": "Qual o prazo para produção de um banner 2x1m?", "status": "new"},
        ]

        for msg_data in messages:
            msg, created = ContactMessage.objects.get_or_create(**msg_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Mensagem de contato criada: {msg.subject}"))
            else:
                self.stdout.write(self.style.WARNING(f"Mensagem de contato já existia: {msg.subject}"))

        self.stdout.write(self.style.SUCCESS("Todos os dados de teste para site criados com sucesso!"))

