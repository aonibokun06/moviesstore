from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import UserProfile

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    REGION_CHOICES = [
        ('', 'Select your region'),
        ('Northeast', 'Northeast'),
        ('Southeast', 'Southeast'),
        ('West', 'West'),
        ('Midwest', 'Midwest'),
        ('Southwest', 'Southwest'),
        ('Pacific Northwest', 'Pacific Northwest'),
    ]
    
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1','password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    REGION_CHOICES = [
        ('', 'Select your region'),
        ('Northeast', 'Northeast'),
        ('Southeast', 'Southeast'),
        ('West', 'West'),
        ('Midwest', 'Midwest'),
        ('Southwest', 'Southwest'),
        ('Pacific Northwest', 'Pacific Northwest'),
    ]
    
    region = forms.ChoiceField(choices=REGION_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['region']