from django.core.management.base import BaseCommand
from popularity.models import Region, MoviePopularity
from movies.models import Movie
import random

class Command(BaseCommand):
    help = 'Populate popularity data with sample regions and movie popularity'

    def handle(self, *args, **options):
        regions_data = [
            {'name': 'Northeast', 'latitude': 42.3601, 'longitude': -71.0589, 'zoom_level': 6},
            {'name': 'Southeast', 'latitude': 33.7490, 'longitude': -84.3880, 'zoom_level': 6},
            {'name': 'West', 'latitude': 34.0522, 'longitude': -118.2437, 'zoom_level': 6},
            {'name': 'Midwest', 'latitude': 41.8781, 'longitude': -87.6298, 'zoom_level': 6},
            {'name': 'Southwest', 'latitude': 33.4484, 'longitude': -112.0740, 'zoom_level': 6},
            {'name': 'Pacific Northwest', 'latitude': 47.6062, 'longitude': -122.3321, 'zoom_level': 6},
        ]

        self.stdout.write('Creating regions...')
        for region_data in regions_data:
            region, created = Region.objects.get_or_create(
                name=region_data['name'],
                defaults=region_data
            )
            if created:
                self.stdout.write(f'Created region: {region.name}')

        self.stdout.write('Creating movie popularity data...')
        movies = Movie.objects.all()
        regions = Region.objects.all()

        for movie in movies:
            for region in regions:
                purchase_count = random.randint(5, 50)
                view_count = random.randint(10, 100)
                
                popularity, created = MoviePopularity.objects.get_or_create(
                    movie=movie,
                    region=region,
                    defaults={
                        'purchase_count': purchase_count,
                        'view_count': view_count
                    }
                )
                if created:
                    self.stdout.write(f'Created popularity data for {movie.name} in {region.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated popularity data!')
        )
