from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Item, UserProfile, Comment, Message
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

# Customize the admin site header and title
admin.site.site_header = "Lost & Found Portal Administration"
admin.site.site_title = "Lost & Found Admin"
admin.site.index_title = "Welcome to Lost & Found Portal Administration"

# Enhanced Item Admin
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'location', 'date', 'status', 'created_display', 'image_preview')
    list_filter = ('category', 'status', 'date', 'user')
    search_fields = ('title', 'description', 'location', 'contact_info', 'user__username')
    list_editable = ('status',)
    readonly_fields = ('image_preview', 'created_display')
    date_hierarchy = 'date'
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'status')
        }),
        ('Location & Contact', {
            'fields': ('location', 'contact_info', 'date')
        }),
        ('User & Matching', {
            'fields': ('user', 'matched_lost_item')
        }),
        ('Media', {
            'fields': ('image', 'image_preview')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 100px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def created_display(self, obj):
        return obj.date.strftime("%B %d, %Y")
    created_display.short_description = "Date Created"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'matched_lost_item')

# Enhanced UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'user_date_joined', 'has_avatar', 'bio_preview')
    list_filter = ('user__date_joined', 'user__is_active')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('avatar_preview', 'user_info')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'user_info')
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar', 'avatar_preview')
        }),
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "Email"
    
    def user_date_joined(self, obj):
        return obj.user.date_joined.strftime("%B %d, %Y")
    user_date_joined.short_description = "Date Joined"
    
    def has_avatar(self, obj):
        return bool(obj.avatar)
    has_avatar.boolean = True
    has_avatar.short_description = "Has Avatar"
    
    def bio_preview(self, obj):
        if obj.bio:
            return obj.bio[:50] + "..." if len(obj.bio) > 50 else obj.bio
        return "No Bio"
    bio_preview.short_description = "Bio Preview"
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 50%;" />',
                obj.avatar.url
            )
        return "No Avatar"
    avatar_preview.short_description = "Avatar Preview"
    
    def user_info(self, obj):
        user_link = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html(
            '<a href="{}">{}</a> ({})',
            user_link, obj.user.username, obj.user.email
        )
    user_info.short_description = "User Details"

# Enhanced Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_title', 'content_preview', 'created_at', 'item_category')
    list_filter = ('created_at', 'item__category', 'user')
    search_fields = ('content', 'user__username', 'item__title')
    readonly_fields = ('created_at', 'item_link', 'user_link')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Comment Details', {
            'fields': ('user_link', 'item_link', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    
    def item_title(self, obj):
        return obj.item.title
    item_title.short_description = "Item"
    
    def item_category(self, obj):
        return obj.item.category
    item_category.short_description = "Category"
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = "Comment"
    
    def item_link(self, obj):
        item_link = reverse('admin:portal_item_change', args=[obj.item.id])
        return format_html('<a href="{}">{}</a>', item_link, obj.item.title)
    item_link.short_description = "Item"
    
    def user_link(self, obj):
        user_link = reverse('admin:auth_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', user_link, obj.user.username)
    user_link.short_description = "User"

# Enhanced Message Admin
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'item_title', 'content_preview', 'created_at', 'is_read', 'item_category')
    list_filter = ('created_at', 'is_read', 'item__category')
    search_fields = ('content', 'sender__username', 'recipient__username', 'item__title')
    readonly_fields = ('created_at', 'item_link', 'sender_link', 'recipient_link')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Message Details', {
            'fields': ('sender_link', 'recipient_link', 'item_link', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def item_title(self, obj):
        return obj.item.title
    item_title.short_description = "Item"
    
    def item_category(self, obj):
        return obj.item.category
    item_category.short_description = "Category"
    
    def content_preview(self, obj):
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content
    content_preview.short_description = "Message"
    
    def item_link(self, obj):
        item_link = reverse('admin:portal_item_change', args=[obj.item.id])
        return format_html('<a href="{}">{}</a>', item_link, obj.item.title)
    item_link.short_description = "Related Item"
    
    def sender_link(self, obj):
        user_link = reverse('admin:auth_user_change', args=[obj.sender.id])
        return format_html('<a href="{}">{}</a>', user_link, obj.sender.username)
    sender_link.short_description = "Sender"
    
    def recipient_link(self, obj):
        user_link = reverse('admin:auth_user_change', args=[obj.recipient.id])
        return format_html('<a href="{}">{}</a>', user_link, obj.recipient.username)
    recipient_link.short_description = "Recipient"

# Enhanced User Admin (extending Django's default UserAdmin)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'items_count', 'messages_count')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    
    def items_count(self, obj):
        return obj.item_set.count()
    items_count.short_description = "Items Posted"
    
    def messages_count(self, obj):
        return obj.sent_messages.count() + obj.received_messages.count()
    messages_count.short_description = "Messages"
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('item_set', 'sent_messages', 'received_messages')

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)