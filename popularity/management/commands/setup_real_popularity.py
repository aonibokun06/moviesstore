from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from popularity.models import Region, MoviePopularity
from cart.models import Order, Item

class Command(BaseCommand):
    help = 'Set up real popularity data by assigning regions to users and updating popularity counts'

    def handle(self, *args, **options):
        regions = ['Northeast', 'Southeast', 'West', 'Midwest', 'Southwest', 'Pacific Northwest']
        
        self.stdout.write('Setting up user regions...')
        
        # Assign regions to existing users
        users = User.objects.all()
        for i, user in enumerate(users):
            region_name = regions[i % len(regions)]  # Cycle through regions
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'region': region_name}
            )
            if not created:
                profile.region = region_name
                profile.save()
            
            self.stdout.write(f'Assigned {user.username} to {region_name}')

        self.stdout.write('Updating popularity data with real purchase data...')
        
        # Reset all popularity data
        MoviePopularity.objects.all().update(purchase_count=0, view_count=0)
        
        # Update popularity based on real orders
        orders = Order.objects.all()
        total_orders = orders.count()
        
        for order in orders:
            try:
                user_profile = UserProfile.objects.get(user=order.user)
                user_region_name = user_profile.region
                
                if user_region_name:
                    try:
                        region = Region.objects.get(name=user_region_name)
                        
                        items = Item.objects.filter(order=order)
                        for item in items:
                            popularity, created = MoviePopularity.objects.get_or_create(
                                movie=item.movie,
                                region=region,
                                defaults={'purchase_count': 0, 'view_count': 0}
                            )
                            popularity.purchase_count += item.quantity
                            popularity.save()
                    except Region.DoesNotExist:
                        continue
            except UserProfile.DoesNotExist:
                continue
        
        self.stdout.write(f'Processed {total_orders} orders')
        self.stdout.write(
            self.style.SUCCESS('Successfully set up real popularity data!')
        )
