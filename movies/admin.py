from django.contrib import admin
from .models import Movie, Review, Rating

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'rating', 'created_at', 'updated_at')
    can_delete = False

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']
    list_display = ('name', 'price', 'average_rating_display', 'total_ratings_display')
    inlines = [RatingInline]
    
    def average_rating_display(self, obj):
        return f"{obj.average_rating():.1f}"
    average_rating_display.short_description = 'Average Rating'
    
    def total_ratings_display(self, obj):
        return obj.total_ratings()
    total_ratings_display.short_description = 'Total Ratings'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__name', 'user__username')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
