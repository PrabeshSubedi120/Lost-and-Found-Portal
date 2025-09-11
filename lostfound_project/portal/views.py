from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, UserProfile, Comment, Message
from .forms import ItemForm, RegisterForm, UserProfileForm, CommentForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count, Q
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def home(request):
    items = Item.objects.all().order_by('-id')
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    query = request.GET.get('q')
    if query:
        items = items.filter(title__icontains=query)
    location = request.GET.get('location')
    if location:
        items = items.filter(location__iexact=location)
    user_count = User.objects.count()
    # Only count found items that are linked to a lost item
    recovered_count = Item.objects.filter(category='Found', matched_lost_item__isnull=False).count()
    return render(request, 'portal/home.html', {
        'items': items,
        'user_count': user_count,
        'recovered_count': recovered_count,
    })

@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            # Set status and handle matching
            if item.category == 'Found' and item.matched_lost_item:
                # Mark the matched lost item as Recovered
                item.matched_lost_item.status = 'Recovered'
                item.matched_lost_item.save()
                item.status = 'Recovered'
            elif item.category == 'Lost':
                item.status = 'Open'
            item.save()
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'portal/add_item.html', {'form': form})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user != request.user:
        return HttpResponseForbidden('You are not allowed to edit this item.')
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_detail', pk=item.pk)
        else:
            print('EDIT FORM ERRORS:', form.errors)
    else:
        form = ItemForm(instance=item)
    return render(request, 'portal/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.user != request.user:
        return HttpResponseForbidden('You are not allowed to delete this item.')
    if request.method == 'POST':
        item.delete()
        return redirect('home')
    return render(request, 'portal/delete_item_confirm.html', {'item': item})

def item_detail(request, pk):
    item = Item.objects.get(pk=pk)
    comment_form = CommentForm()
    message_form = MessageForm()
    comments = item.comments.all().order_by('-created_at')
    messages_qs = item.messages.all().order_by('-created_at')
    return render(request, 'portal/item_detail.html', {
        'item': item,
        'comment_form': comment_form,
        'message_form': message_form,
        'comments': comments,
        'messages': messages_qs,
    })

def register(request):
    # Clear admin-related messages that shouldn't appear on register page
    storage = messages.get_messages(request)
    filtered_messages = []
    for message in storage:
        # Keep only registration-related messages
        if any(keyword in str(message).lower() for keyword in ['registration', 'account', 'username', 'password', 'email']):
            filtered_messages.append(message)
    
    # Clear the message storage and add back only filtered messages
    storage.used = True
    for msg in filtered_messages:
        messages.add_message(request, msg.level, msg.message, msg.tags)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in to continue.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'portal/register.html', {'form': form})

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'portal/profile.html', {'form': form, 'profile': profile})

@login_required
def dashboard(request):
    user_items = Item.objects.filter(user=request.user)
    recovered_count = user_items.filter(status='Recovered').count()
    lost_count = user_items.filter(category='Lost').count()
    found_count = user_items.filter(category='Found').count()
    comments_count = Comment.objects.filter(user=request.user).count()
    messages_count = Message.objects.filter(recipient=request.user).count()
    return render(request, 'portal/dashboard.html', {
        'user_items': user_items,
        'recovered_count': recovered_count,
        'lost_count': lost_count,
        'found_count': found_count,
        'comments_count': comments_count,
        'messages_count': messages_count,
    })

@login_required
def add_comment(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.item = item
            comment.save()
            messages.success(request, 'Comment added!')
    return redirect('item_detail', pk=item_id)

@login_required
def send_message(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.user == item.user:
        return HttpResponseForbidden('You cannot claim your own item.')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = item.user
            msg.item = item
            msg.save()
            messages.success(request, 'Message sent to item owner!')
    return redirect('item_detail', pk=item_id)

@login_required
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'portal/inbox.html', {'messages': messages_received})

# ============== CUSTOM AUTHENTICATION VIEWS ==============

def custom_login(request):
    """Custom login view that clears admin sessions"""
    # Clear admin-related messages that shouldn't appear on login page
    storage = messages.get_messages(request)
    filtered_messages = []
    for message in storage:
        # Keep only registration-related or login-related messages
        if any(keyword in str(message).lower() for keyword in ['registration successful', 'logout successful', 'invalid username', 'welcome back']):
            filtered_messages.append(message)
    
    # Clear the message storage and add back only filtered messages
    storage.used = True
    for msg in filtered_messages:
        messages.add_message(request, msg.level, msg.message, msg.tags)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Clear any existing admin session
                if 'is_admin_authenticated' in request.session:
                    del request.session['is_admin_authenticated']
                if 'admin_username' in request.session:
                    del request.session['admin_username']
                if 'admin_email' in request.session:
                    del request.session['admin_email']
                
                # Login the user
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                
                # Redirect to next or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'portal/login.html', {'form': form})

def custom_logout(request):
    """Custom logout view that clears both user and admin sessions"""
    # Clear admin session if exists
    if 'is_admin_authenticated' in request.session:
        del request.session['is_admin_authenticated']
    if 'admin_username' in request.session:
        del request.session['admin_username']
    if 'admin_email' in request.session:
        del request.session['admin_email']
    
    # Logout user
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

# ============== CUSTOM ADMIN VIEWS ==============

def admin_required(view_func):
    """Custom decorator for admin authentication using .env credentials"""
    def wrapper(request, *args, **kwargs):
        # Check if admin is authenticated
        if not request.session.get('is_admin_authenticated'):
            messages.warning(request, 'Admin authentication required.')
            return redirect('admin_login')
        
        # Additional security: ensure no regular user is logged in while accessing admin
        if request.user.is_authenticated:
            logout(request)
            messages.warning(request, 'User session cleared for admin access.')
        
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    """Custom admin dashboard with statistics and overview"""
    # Get statistics
    total_users = User.objects.count()
    total_items = Item.objects.count()
    total_lost = Item.objects.filter(category='Lost').count()
    total_found = Item.objects.filter(category='Found').count()
    total_recovered = Item.objects.filter(status='Recovered').count()
    total_comments = Comment.objects.count()
    total_messages = Message.objects.count()
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_users = User.objects.filter(date_joined__gte=week_ago).count()
    recent_items = Item.objects.filter(date__gte=week_ago.date()).count()
    recent_comments = Comment.objects.filter(created_at__gte=week_ago).count()
    recent_messages = Message.objects.filter(created_at__gte=week_ago).count()
    
    # Recent items for quick overview
    recent_items_list = Item.objects.select_related('user').order_by('-id')[:5]
    recent_users_list = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'total_items': total_items,
        'total_lost': total_lost,
        'total_found': total_found,
        'total_recovered': total_recovered,
        'total_comments': total_comments,
        'total_messages': total_messages,
        'recent_users': recent_users,
        'recent_items': recent_items,
        'recent_comments': recent_comments,
        'recent_messages': recent_messages,
        'recent_items_list': recent_items_list,
        'recent_users_list': recent_users_list,
    }
    return render(request, 'portal/admin_dashboard.html', context)

@admin_required
def admin_users(request):
    """Manage all users"""
    search_query = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')
    
    users = User.objects.all().select_related('profile').annotate(
        items_count=Count('item'),
        comments_count=Count('comment'),
        messages_sent=Count('sent_messages'),
        messages_received=Count('received_messages')
    ).order_by('-date_joined')
    
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    if filter_type == 'staff':
        users = users.filter(is_staff=True)
    elif filter_type == 'active':
        users = users.filter(is_active=True)
    elif filter_type == 'inactive':
        users = users.filter(is_active=False)
    
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    return render(request, 'portal/admin_users.html', {
        'users': users_page,
        'search_query': search_query,
        'filter_type': filter_type,
    })

@admin_required
def admin_items(request):
    """Manage all items"""
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', 'all')
    status_filter = request.GET.get('status', 'all')
    
    items = Item.objects.all().select_related('user')
    
    if search_query:
        items = items.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    if category_filter != 'all':
        items = items.filter(category=category_filter)
    
    if status_filter != 'all':
        items = items.filter(status=status_filter)
    
    paginator = Paginator(items, 15)
    page_number = request.GET.get('page')
    items_page = paginator.get_page(page_number)
    
    return render(request, 'portal/admin_items.html', {
        'items': items_page,
        'search_query': search_query,
        'category_filter': category_filter,
        'status_filter': status_filter,
    })

@admin_required
def admin_comments(request):
    """Manage all comments"""
    search_query = request.GET.get('search', '')
    
    comments = Comment.objects.all().select_related('user', 'item')
    
    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(item__title__icontains=search_query)
        )
    
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    comments_page = paginator.get_page(page_number)
    
    return render(request, 'portal/admin_comments.html', {
        'comments': comments_page,
        'search_query': search_query,
    })

@admin_required
def admin_messages(request):
    """Manage all messages"""
    search_query = request.GET.get('search', '')
    read_filter = request.GET.get('read', 'all')
    
    messages_qs = Message.objects.all().select_related('sender', 'recipient', 'item')
    
    if search_query:
        messages_qs = messages_qs.filter(
            Q(content__icontains=search_query) |
            Q(sender__username__icontains=search_query) |
            Q(recipient__username__icontains=search_query) |
            Q(item__title__icontains=search_query)
        )
    
    if read_filter == 'read':
        messages_qs = messages_qs.filter(is_read=True)
    elif read_filter == 'unread':
        messages_qs = messages_qs.filter(is_read=False)
    
    paginator = Paginator(messages_qs, 20)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    return render(request, 'portal/admin_messages.html', {
        'messages': messages_page,
        'search_query': search_query,
        'read_filter': read_filter,
    })

@admin_required
def admin_user_toggle_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    
    status = "activated" if user.is_active else "deactivated"
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('admin_users')

@admin_required
@admin_required
def admin_delete_user(request, user_id):
    """Delete a user account"""
    user = get_object_or_404(User, id=user_id)
    
    # Safety check: prevent deletion of superusers
    if user.is_superuser:
        messages.error(request, f'Cannot delete superuser account: {user.username}')
        return redirect('admin_users')
    
    # Safety check: prevent deletion of the current admin (if they're a regular user)
    current_admin_username = request.session.get('admin_username')
    if user.username == current_admin_username:
        messages.error(request, 'Cannot delete your own account while logged in as admin.')
        return redirect('admin_users')
    
    # Store user info before deletion
    username = user.username
    
    # Delete associated profile if exists
    if hasattr(user, 'profile'):
        user.profile.delete()
    
    # Delete the user (Django will cascade delete related items, comments, messages)
    user.delete()
    
    # Create concise success message for admin dashboard only
    messages.success(request, f'User "{username}" has been successfully deleted.')
    return redirect('admin_users')

@admin_required
def admin_item_toggle_status(request, item_id):
    """Toggle item status between Open and Recovered"""
    item = get_object_or_404(Item, id=item_id)
    item.status = 'Recovered' if item.status == 'Open' else 'Open'
    item.save()
    
    messages.success(request, f'Item "{item.title}" status changed to {item.status}.')
    return redirect('admin_items')

@admin_required
def admin_delete_comment(request, comment_id):
    """Delete a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Comment has been deleted.')
    return redirect('admin_comments')

@admin_required
def admin_delete_message(request, message_id):
    """Delete a message"""
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    messages.success(request, 'Message has been deleted.')
    return redirect('admin_messages')

@admin_required
def admin_delete_item(request, item_id):
    """Delete an item"""
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.success(request, f'Item "{item.title}" has been deleted.')
    return redirect('admin_items')

# ============== CUSTOM ADMIN AUTHENTICATION ==============

def admin_login(request):
    """Custom admin login using .env credentials"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check against .env credentials
        if (username == settings.ADMIN_USERNAME and 
            password == settings.ADMIN_PASSWORD):
            
            # Clear any existing user session
            if request.user.is_authenticated:
                logout(request)
            
            # Clear all messages from previous sessions
            storage = messages.get_messages(request)
            storage.used = True
            
            # Create session for admin access
            request.session['is_admin_authenticated'] = True
            request.session['admin_username'] = username
            request.session['admin_email'] = settings.ADMIN_EMAIL
            
            # Add success message only for admin dashboard
            messages.success(request, f'Welcome {username}! Admin access granted.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials. Please try again.')
    
    return render(request, 'portal/admin_login.html')

def admin_logout(request):
    """Logout from admin session"""
    if 'is_admin_authenticated' in request.session:
        del request.session['is_admin_authenticated']
    if 'admin_username' in request.session:
        del request.session['admin_username']
    if 'admin_email' in request.session:
        del request.session['admin_email']
    
    # Don't add a message here as it might confuse users on other pages
    return redirect('home')

