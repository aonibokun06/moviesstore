from django.contrib import admin
from .models import Region, MoviePopularity

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'zoom_level')
    search_fields = ('name',)

@admin.register(MoviePopularity)
class MoviePopularityAdmin(admin.ModelAdmin):
    list_display = ('movie', 'region', 'purchase_count', 'view_count', 'total_popularity', 'last_updated')
    list_filter = ('region', 'last_updated')
    search_fields = ('movie__name', 'region__name')
    
    def total_popularity(self, obj):
        return obj.total_popularity()
    total_popularity.short_description = 'Total Popularity' 