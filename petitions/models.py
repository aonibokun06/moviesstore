from django.db import models
from django.contrib.auth.models import User

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    movie_title = models.CharField(max_length=200, help_text="The movie title you want to add to the catalog")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.movie_title}"
    
    @property
    def yes_votes(self):
        return self.vote_set.filter(vote_type='yes').count()
    
    @property
    def no_votes(self):
        return self.vote_set.filter(vote_type='no').count()
    
    @property
    def total_votes(self):
        return self.vote_set.count()

class Vote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['petition', 'user']
    
    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on {self.petition.title}"
