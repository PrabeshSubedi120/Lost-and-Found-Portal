from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Remove default admin superuser and clean up unwanted accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Actually delete the users (without this flag, it will only show what would be deleted)',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Specific username to delete',
        )

    def handle(self, *args, **options):
        # Default unwanted usernames (common defaults created during development)
        unwanted_usernames = ['admin', 'test', 'testuser', 'root']
        
        if options['username']:
            # Delete specific username
            unwanted_usernames = [options['username']]
        
        found_users = []
        
        for username in unwanted_usernames:
            try:
                user = User.objects.get(username=username)
                found_users.append(user)
                self.stdout.write(
                    f"Found user: {user.username} (Email: {user.email}, Superuser: {user.is_superuser}, Joined: {user.date_joined})"
                )
            except User.DoesNotExist:
                continue
        
        if not found_users:
            self.stdout.write(
                self.style.SUCCESS('No unwanted default users found.')
            )
            return
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING('\n--- DRY RUN MODE ---')
            )
            self.stdout.write(
                f"Found {len(found_users)} user(s) that would be deleted."
            )
            self.stdout.write(
                "Run with --confirm to actually delete these users."
            )
            return
        
        # Actually delete the users
        deleted_count = 0
        for user in found_users:
            username = user.username
            user_email = user.email
            
            # Delete associated profile if exists
            if hasattr(user, 'profile'):
                user.profile.delete()
                self.stdout.write(f"Deleted profile for user: {username}")
            
            # Delete the user (Django will cascade delete related items, comments, messages)
            user.delete()
            deleted_count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted user: {username} ({user_email})')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nDeleted {deleted_count} unwanted user(s) successfully.')
        )
        self.stdout.write(
            'Your custom admin authentication system is unaffected.'
        )