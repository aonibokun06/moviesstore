from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Region, MoviePopularity
from movies.models import Movie
from cart.models import Order, Item

def popularity_map(request):
    regions = Region.objects.all()
    template_data = {
        'title': 'Local Popularity Map',
        'regions': regions,
    }
    return render(request, 'popularity/map.html', {'template_data': template_data})

def region_details(request, region_id):
    region = get_object_or_404(Region, id=region_id)
    popular_movies = MoviePopularity.objects.filter(region=region).order_by('-purchase_count')[:10]
    
    # Find the movie with highest total popularity for trending tag
    trending_movie_id = None
    if popular_movies:
        max_popularity = 0
        for movie_pop in popular_movies:
            total_pop = movie_pop.purchase_count + movie_pop.view_count
            if total_pop > max_popularity:
                max_popularity = total_pop
                trending_movie_id = movie_pop.movie.id
    
    template_data = {
        'title': f'Popular Movies in {region.name}',
        'region': region,
        'popular_movies': popular_movies,
        'trending_movie_id': trending_movie_id,
    }
    return render(request, 'popularity/region_details.html', {'template_data': template_data})

def update_popularity_data(request):
    if request.method == 'POST':
        from django.utils import timezone
        from accounts.models import UserProfile
        
        # Reset all popularity data to 0 first
        MoviePopularity.objects.all().update(purchase_count=0, view_count=0)
        
        # Get all orders and update popularity based on user regions
        orders = Order.objects.all()
        
        for order in orders:
            try:
                # Get user's region from profile
                user_profile = UserProfile.objects.get(user=order.user)
                user_region_name = user_profile.region
                
                if user_region_name:
                    # Find the matching region
                    try:
                        region = Region.objects.get(name=user_region_name)
                        
                        # Update popularity for each item in the order
                        items = Item.objects.filter(order=order)
                        for item in items:
                            popularity, created = MoviePopularity.objects.get_or_create(
                                movie=item.movie,
                                region=region,
                                defaults={'purchase_count': 0, 'view_count': 0}
                            )
                            popularity.purchase_count += item.quantity
                            popularity.save()
                    except Region.DoesNotExist:
                        # Skip if region doesn't exist
                        continue
            except UserProfile.DoesNotExist:
                # Skip if user doesn't have a profile/region
                continue
        
        return JsonResponse({'status': 'success', 'message': 'Popularity data updated with real purchase data'})
    
    return JsonResponse({'status': 'error'})