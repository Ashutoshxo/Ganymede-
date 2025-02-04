# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import SubscriptionPlan

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Enter Username',
            'email': 'Enter Email',
            'password1': 'Enter Password',
            'password2': 'Confirm Password',
        }

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Enter Username"
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Enter Email"
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Enter PASSWORD"
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Confirm PASSWORD"
        })
    )



#login
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-warning border-warning',
            'placeholder': 'Enter Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-warning border-warning',
            'placeholder': 'Enter Password'
        })
    )
   



class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['plan']

    plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )  




# from .models import CustomUser

# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['bio', 'profile_picture']  




from django.contrib.auth.forms import UserChangeForm


class UserProfileForm(UserChangeForm):
    
    password = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'bio']




from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'release_date', 'genre', 'duration', 'image', 'music_file']  

from django.forms import ModelForm
from . models import Album
class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist', 'release_date', 'cover_image']
       
        




from django import forms
from .models import FavoriteSong, FavoriteAlbum

class FavoriteSongForm(forms.ModelForm):
    class Meta:
        model = FavoriteSong
        fields = ['song']  # Assuming `song` is the field in the FavoriteSong model

class FavoriteAlbumForm(forms.ModelForm):
    class Meta:
        model = FavoriteAlbum
        fields = ['album']  # Assuming `album` is the field in the FavoriteAlbum model

# forms.py

from .models import ArtistFollow, Artist

class ArtistFollowForm(forms.ModelForm):
    class Meta:
        model = ArtistFollow
        fields = ['artist']
