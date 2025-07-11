from django.contrib import admin
from .models import Item, UserProfile, Comment, Message

# Register your models here.

admin.site.register(Item)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Message)