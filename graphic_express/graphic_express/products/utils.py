from decimal import Decimal

def calculate_product_price(product, quantity):
    """
    Calcula o preço do produto baseado na quantidade solicitada
    usando as regras de preço definidas
    """
    if quantity < product.min_quantity:
        raise ValueError(f"Quantidade mínima é {product.min_quantity}")
    
    if quantity > product.max_quantity:
        raise ValueError(f"Quantidade máxima é {product.max_quantity}")
    
    # Encontrar a regra de preço apropriada
    price_rule = product.price_rules.filter(
        min_quantity__lte=quantity,
        max_quantity__gte=quantity
    ).first()
    
    if not price_rule:
        # Buscar a última regra onde min_quantity <= quantidade
        price_rule = product.price_rules.filter(
            min_quantity__lte=quantity
        ).order_by('-min_quantity').first()
    
    if price_rule:
        return price_rule.price * quantity
    else:
        return product.base_price * quantity