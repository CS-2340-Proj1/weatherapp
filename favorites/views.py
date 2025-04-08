from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required
def index(request):
    fav_total = 0
    cities_in_fav = []
    favlist = request.session.get('favorites', {})
    movie_ids = list(favlist.keys())
    if (movie_ids != []):
        cities_in_fav = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(favlist, cities_in_fav)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = cities_in_fav
    template_data['cart_total'] = fav_total
    return render(request, 'favorites/index.html',{'template_data': template_data})
def add(request, id):
    get_object_or_404(Movie, id=id)
    cart = request.session.get('favorites', {})
    cart[id] = request.POST['quantity']
    request.session['favorites'] = cart
    return redirect('favorites.index')
def clear(request):
    request.session['favorites'] = {}
    return redirect('favorites.index')
@login_required
def purchase(request):
    cart = request.session.get('favorites', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('favorites.index')
    cities_in_fav = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, cities_in_fav)
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    for movie in cities_in_fav:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    request.session['favorites'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'favorites/purchase.html',
        {'template_data': template_data})