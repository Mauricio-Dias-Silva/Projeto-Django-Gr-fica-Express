from django.core.management.base import BaseCommand
from products.models import Category, Product, PriceRule

class Command(BaseCommand):
    help = 'Cria dados iniciais para teste'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando criação de dados de teste...")

        # Função auxiliar para criar ou obter objetos
        def create_or_get(model, defaults=None, **kwargs):
            obj, created = model.objects.get_or_create(**kwargs, defaults=defaults or {})
            if created:
                self.stdout.write(self.style.SUCCESS(f"{model.__name__} '{obj}' criado."))
            else:
                self.stdout.write(self.style.WARNING(f"{model.__name__} '{obj}' já existia."))
            return obj

        # Criar categorias
        cat1 = create_or_get(Category,
            name="Cartões de Visita",
            slug="cartoes-visita",
            defaults={'description': 'Cartões de visita personalizados'}
        )
        cat2 = create_or_get(Category,
            name="Flyers e Panfletos",
            slug="flyers-panfletos",
            defaults={'description': 'Flyers e panfletos promocionais'}
        )
        cat3 = create_or_get(Category,
            name="Banners",
            slug="banners",
            defaults={'description': 'Banners de diversos tamanhos'}
        )

        # Criar produtos
        product1 = create_or_get(Product,
            name="Cartão de Visita Standard",
            slug="cartao-visita-standard",
            defaults={
                'category': cat1,
                'description': 'Cartão de visita em papel couchê 300g, frente e verso colorido',
                'base_price': 29.90,
                'available': True
            }
        )

        product2 = create_or_get(Product,
            name="Flyer A4 Colorido",
            slug="flyer-a4-colorido",
            defaults={
                'category': cat2,
                'description': 'Flyer em papel couchê 150g, formato A4, impressão colorida',
                'base_price': 49.90,
                'available': True
            }
        )

        product3 = create_or_get(Product,
            name="Banner Lona 1x1m",
            slug="banner-lona-1x1m",
            defaults={
                'category': cat3,
                'description': 'Banner em lona com ilhós, tamanho 1x1 metro',
                'base_price': 89.90,
                'available': True
            }
        )

        # Criar regras de preço
        price_rules = [
            # Regras para Cartão de Visita
            {'product': product1, 'min_quantity': 100, 'max_quantity': 499, 'price': 0.12},
            {'product': product1, 'min_quantity': 500, 'max_quantity': 999, 'price': 0.09},
            {'product': product1, 'min_quantity': 1000, 'price': 0.07},
            # Regras para Flyer
            {'product': product2, 'min_quantity': 100, 'max_quantity': 499, 'price': 0.40},
            {'product': product2, 'min_quantity': 500, 'max_quantity': 999, 'price': 0.35},
            {'product': product2, 'min_quantity': 1000, 'price': 0.30},
            # Regras para Banner
            {'product': product3, 'min_quantity': 10, 'max_quantity': 49, 'price': 75.00},
            {'product': product3, 'min_quantity': 50, 'max_quantity': 99, 'price': 70.00},
            {'product': product3, 'min_quantity': 100, 'price': 65.00},
        ]

        for rule in price_rules:
            pr, created = PriceRule.objects.get_or_create(
                product=rule['product'],
                min_quantity=rule['min_quantity'],
                max_quantity=rule.get('max_quantity'),
                defaults={'price': rule['price']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Regra de preço criada para {rule['product']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Regra de preço já existia para {rule['product']}"))

        self.stdout.write(self.style.SUCCESS("Todos os dados iniciais criados com sucesso!"))
