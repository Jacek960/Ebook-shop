from django import template
from books.models import Cart

register = template.Library()

@register.filter
def cart_products_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user)
        if qs.exists():
            return qs[0].product.count()
        return 0

