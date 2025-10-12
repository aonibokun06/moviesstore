from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Region(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    zoom_level = models.IntegerField(default=10)
    
    def __str__(self):
        return self.name

class MoviePopularity(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    purchase_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('movie', 'region')
    
    def __str__(self):
        return f"{self.movie.name} in {self.region.name} - {self.purchase_count} purchases"
    
    def total_popularity(self):
        return self.purchase_count + self.view_count