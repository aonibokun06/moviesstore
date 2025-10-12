from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Rating
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    user_rating = movie.user_rating(request.user)
    
    # Track movie view for popularity
    if request.user.is_authenticated:
        try:
            from accounts.models import UserProfile
            user_profile = UserProfile.objects.get(user=request.user)
            user_region_name = user_profile.region
            
            if user_region_name:
                try:
                    from popularity.models import Region, MoviePopularity
                    region = Region.objects.get(name=user_region_name)
                    popularity, created = MoviePopularity.objects.get_or_create(
                        movie=movie,
                        region=region,
                        defaults={'purchase_count': 0, 'view_count': 0}
                    )
                    popularity.view_count += 1
                    popularity.save()
                except:
                    # Skip if popularity models not available
                    pass
        except:
            # Skip if user profile doesn't exist
            pass
    
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['user_rating'] = user_rating
    return render(request, 'movies/show.html', {'template_data': template_data})

