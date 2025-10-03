from django.contrib import admin
from .models import Petition, Vote

@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'created_by', 'yes_votes', 'no_votes', 'total_votes', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'movie_title', 'description', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Petition Details', {
            'fields': ('title', 'movie_title', 'description', 'is_active')
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at']
    search_fields = ['user__username', 'petition__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
