#!/usr/bin/env python
\"\"\"
Quick script to remove the unwanted default 'admin' superuser
Run this from the lostfound_project directory: python remove_admin_user.py
\"\"\"

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lostfound_project.settings')
django.setup()

from django.contrib.auth.models import User

def remove_admin_user():
    try:
        # Find the unwanted admin user
        admin_user = User.objects.get(username='admin')
        
        print(f"Found user: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Is superuser: {admin_user.is_superuser}")
        print(f"Date joined: {admin_user.date_joined}")
        print(f"Items count: {admin_user.item_set.count()}")
        
        # Ask for confirmation
        confirm = input("\\nAre you sure you want to delete this user? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y']:
            # Delete associated profile if exists
            if hasattr(admin_user, 'profile'):
                admin_user.profile.delete()
                print("Deleted associated profile.")
            
            # Delete the user
            admin_user.delete()
            print(f"✅ Successfully deleted user '{admin_user.username}'!")
            print("Your custom admin system (iamprabesh) is unaffected.")
            
        else:
            print("❌ User deletion cancelled.")
            
    except User.DoesNotExist:
        print("✅ No 'admin' user found. Your system is clean!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧹 Cleaning up unwanted default admin user...")
    print("=" * 50)
    remove_admin_user()