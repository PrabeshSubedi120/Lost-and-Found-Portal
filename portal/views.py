from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, UserProfile, Comment, Message
from .forms import ItemForm, RegisterForm, UserProfileForm, CommentForm, MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Count

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

