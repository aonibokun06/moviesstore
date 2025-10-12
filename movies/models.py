from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
    def average_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0
    
    def average_rating_display(self):
        avg = self.average_rating()
        return int(avg)
    
    def has_half_star(self):
        avg = self.average_rating()
        return avg - int(avg) >= 0.5
    
    def total_ratings(self):
        return self.rating_set.count()
    
    def user_rating(self, user):
        if user.is_authenticated:
            try:
                return self.rating_set.get(user=user).rating
            except Rating.DoesNotExist:
                return None
        return None

