from django import forms
from .models import Item, UserProfile, Comment, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import datetime

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['user', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show open Lost items for matching
        self.fields['matched_lost_item'].queryset = Item.objects.filter(category='Lost', status='Open')
        self.fields['matched_lost_item'].required = False
        self.fields['matched_lost_item'].label = 'Match to Lost Item (optional)'
        # Set default date to today if not already set
        if not self.initial.get('date') and not self.data.get('date'):
            self.initial['date'] = datetime.date.today()
        # Ensure image is never required
        self.fields['image'].required = False

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your message...'}),
        }
