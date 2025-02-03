# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser  # Import your custom user model
from .models import SubscriptionPlan

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser  # Use your custom user model here
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'username': 'Enter Username',
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
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
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Enter First Name"
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control bg-dark text-warning border-warning",
            "placeholder": "Enter Last Name"
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
   


#sub
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ['plan']

    plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )  




from django import forms
from .models import CustomUser

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture']  


# forms.py
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class UserProfileForm(UserChangeForm):
    # Exclude the password field from the form
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
