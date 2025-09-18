from django import template
register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(carts, movie_id):
    for cart_id, cart in carts.items():
        if str(movie_id) in cart:
            return cart[str(movie_id)]
    return 0