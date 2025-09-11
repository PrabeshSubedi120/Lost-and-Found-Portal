from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_item, name='add_item'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:pk>/edit/', views.edit_item, name='edit_item'),
    path('item/<int:pk>/delete/', views.delete_item, name='delete_item'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    # New profile/dashboard/comments/messaging URLs
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inbox/', views.inbox, name='inbox'),
    path('item/<int:item_id>/comment/', views.add_comment, name='add_comment'),
    path('item/<int:item_id>/claim/', views.send_message, name='send_message'),
    
    # Custom Admin URLs
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/items/', views.admin_items, name='admin_items'),
    path('admin-panel/comments/', views.admin_comments, name='admin_comments'),
    path('admin-panel/messages/', views.admin_messages, name='admin_messages'),
    
    # Admin Action URLs
    path('admin-panel/users/<int:user_id>/toggle-status/', views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin-panel/users/<int:user_id>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('admin-panel/items/<int:item_id>/toggle-status/', views.admin_item_toggle_status, name='admin_item_toggle_status'),
    path('admin-panel/items/<int:item_id>/delete/', views.admin_delete_item, name='admin_delete_item'),
    path('admin-panel/comments/<int:comment_id>/delete/', views.admin_delete_comment, name='admin_delete_comment'),
    path('admin-panel/messages/<int:message_id>/delete/', views.admin_delete_message, name='admin_delete_message'),
]
