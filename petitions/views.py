from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Petition, Vote

def petition_list(request):
    petitions = Petition.objects.filter(is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(petitions, 10)
    page_number = request.GET.get('page')
    petitions_page = paginator.get_page(page_number)
    
    template_data = {
        'title': 'Movie Petitions - MoviesStore',
        'description': 'Vote on which movies should be added to our catalog',
        'petitions': petitions_page,
    }
    return render(request, 'petitions/list.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(petition=petition, user=request.user)
        except Vote.DoesNotExist:
            user_vote = None
    
    template_data = {
        'title': f'{petition.title} - MoviesStore',
        'description': petition.description,
        'petition': petition,
        'user_vote': user_vote,
    }
    return render(request, 'petitions/detail.html', {'template_data': template_data})

@login_required
def create_petition(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        movie_title = request.POST.get('movie_title', '').strip()
        
        if not title or not description or not movie_title:
            messages.error(request, 'All fields are required.')
        else:
            petition = Petition.objects.create(
                title=title,
                description=description,
                movie_title=movie_title,
                created_by=request.user
            )
            messages.success(request, 'Petition created successfully!')
            return redirect('petitions.detail', petition_id=petition.id)
    
    template_data = {
        'title': 'Create Petition - MoviesStore',
        'description': 'Create a new petition to add a movie to our catalog',
    }
    return render(request, 'petitions/create.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    vote_type = request.POST.get('vote_type')
    
    if vote_type not in ['yes', 'no']:
        messages.error(request, 'Invalid vote type.')
        return redirect('petitions.detail', petition_id=petition.id)
    existing_vote = Vote.objects.filter(petition=petition, user=request.user).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            messages.info(request, 'You have already voted this way.')
        else:
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, f'Your vote has been changed to {vote_type.upper()}.')
    else:
        Vote.objects.create(
            petition=petition,
            user=request.user,
            vote_type=vote_type
        )
        messages.success(request, f'Thank you for voting {vote_type.upper()}!')
    
    return redirect('petitions.detail', petition_id=petition.id)
