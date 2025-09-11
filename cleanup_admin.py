#!/usr/bin/env python
"""
Script to remove unwanted admin user from production database.
Run this on Render after deployment.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'lostfound_project'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound_project.settings_production')
django.setup()

from django.contrib.auth.models import User
from django.conf import settings


def remove_unwanted_admin():
    """Remove the unwanted admin user"""
    
    # Get admin credentials from settings
    admin_username = getattr(settings, 'ADMIN_USERNAME', 'iamprabesh')
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'iamprabesh2003@gmail.com')
    
    print(f"Protected admin user: {admin_username}")
    print("Searching for unwanted admin users...")
    
    # Find users that might be unwanted admins
    unwanted_users = User.objects.filter(
        username='admin'
    ).exclude(username=admin_username)
    
    if not unwanted_users.exists():
        print("No unwanted admin users found.")
        return
    
    for user in unwanted_users:
        print(f"\nFound unwanted user:")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is superuser: {user.is_superuser}")
        print(f"  Is staff: {user.is_staff}")
        print(f"  Date joined: {user.date_joined}")
        
        try:
            user.delete()
            print(f"✓ Successfully deleted user '{user.username}'")
        except Exception as e:
            print(f"✗ Error deleting user '{user.username}': {str(e)}")
    
    print("\nCleanup completed!")


if __name__ == "__main__":
    remove_unwanted_admin()