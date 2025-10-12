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

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def rate_movie(request, id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=id)
        rating_value = request.POST.get('rating')
        
        if rating_value and rating_value.isdigit():
            rating_value = int(rating_value)
            if 1 <= rating_value <= 5:
                rating, created = Rating.objects.get_or_create(
                    movie=movie,
                    user=request.user,
                    defaults={'rating': rating_value}
                )
                if not created:
                    rating.rating = rating_value
                    rating.save()
                    messages.success(request, f'Your rating has been updated to {rating_value} stars!')
                else:
                    messages.success(request, f'Your rating of {rating_value} stars has been saved!')
            else:
                messages.error(request, 'Rating must be between 1 and 5 stars.')
        else:
            messages.error(request, 'Please select a valid rating.')
    
    return redirect('movies.show', id=id)