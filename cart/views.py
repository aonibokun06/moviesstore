from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item, Cart, CartItem
from django.contrib.auth.decorators import login_required

def index(request):
    # Show cart selection page
    template_data = {}
    template_data['title'] = 'Select Cart'
    template_data['carts'] = ['cart_1', 'cart_2', 'cart_3']
    return render(request, 'cart/index.html', {'template_data': template_data})

def view_cart(request, cart_id):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('carts', {}).get(cart_id, {})
    movie_ids = list(cart.keys())
    
    if movie_ids:
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    
    template_data = {}
    template_data['title'] = f'{cart_id.replace("_", " ").title()}'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    template_data['cart_id'] = cart_id
    template_data['all_carts'] = ['cart_1', 'cart_2', 'cart_3']
    
    return render(request, 'cart/view_cart.html', {'template_data': template_data})

def add(request, id, cart_id):
    get_object_or_404(Movie, id=id)
    
    # Initialize carts if they don't exist
    if 'carts' not in request.session:
        request.session['carts'] = {'cart_1': {}, 'cart_2': {}, 'cart_3': {}}
    
    cart = request.session['carts'].get(cart_id, {})
    cart[id] = request.POST['quantity']
    request.session['carts'][cart_id] = cart
    request.session.modified = True
    
    return redirect('cart.view_cart', cart_id=cart_id)

def clear(request, cart_id):
    if 'carts' in request.session:
        request.session['carts'][cart_id] = {}
        request.session.modified = True
    return redirect('cart.view_cart', cart_id=cart_id)

@login_required
def purchase(request, cart_id):
    cart = request.session.get('carts', {}).get(cart_id, {})
    movie_ids = list(cart.keys())
    
    if not movie_ids:
        return redirect('cart.view_cart', cart_id=cart_id)
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)
    
    # Create Order
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    
    # Create Items
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    
    # Clear the specific cart after purchase
    request.session['carts'][cart_id] = {}
    request.session.modified = True
    
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    template_data['cart_id'] = cart_id
    
    return render(request, 'cart/purchase.html', {'template_data': template_data})
