from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    help = 'Remove unwanted admin user from production database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username to delete (default: admin)',
            default='admin'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )

    def handle(self, *args, **options):
        username_to_delete = options['username']
        confirm = options['confirm']
        
        # Get the admin credentials from settings
        admin_username = getattr(settings, 'ADMIN_USERNAME', 'iamprabesh')
        
        try:
            user_to_delete = User.objects.get(username=username_to_delete)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User "{username_to_delete}" does not exist.')
            )
            return

        # Safety check - don't delete the main admin
        if username_to_delete == admin_username:
            self.stdout.write(
                self.style.ERROR(
                    f'Cannot delete the main admin user "{admin_username}". '
                    'This would lock you out of the system!'
                )
            )
            return

        # Show user details
        self.stdout.write(f'User to delete:')
        self.stdout.write(f'  Username: {user_to_delete.username}')
        self.stdout.write(f'  Email: {user_to_delete.email}')
        self.stdout.write(f'  Is superuser: {user_to_delete.is_superuser}')
        self.stdout.write(f'  Is staff: {user_to_delete.is_staff}')
        self.stdout.write(f'  Date joined: {user_to_delete.date_joined}')

        if not confirm:
            confirmation = input(f'\nAre you sure you want to delete user "{username_to_delete}"? (yes/no): ')
            if confirmation.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Deletion cancelled.'))
                return

        # Delete the user
        try:
            user_to_delete.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted user "{username_to_delete}".'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error deleting user: {str(e)}')
            )