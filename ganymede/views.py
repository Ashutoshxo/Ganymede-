from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Q
from .models import SubscriptionPlan, UserSubscription
from .models import Artist, ArtistFollow
from .models import Song , Genre, Album, Playlist
from .models import UserSubscription
from .models import FavoriteSong, FavoriteAlbum, ArtistFollow



from django.contrib.auth.models import User

from .forms import RegisterForm , LoginForm , SubscriptionForm 
from .forms import FavoriteSongForm, FavoriteAlbumForm, ArtistFollowForm
from .forms import SongForm, AlbumForm 

from django.views import View

from django.utils import timezone

from django.urls import reverse

from django.contrib import messages

from datetime import timedelta

import uuid

from django.conf import settings

from paypal.standard.forms import PayPalPaymentsForm 

from django.core.paginator import Paginator


from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required, user_passes_test


from rest_framework import status

from rest_framework.response import Response

from rest_framework.views import APIView

from .serializers import SongSerializer, ArtistSerializer, GenreSerializer, AlbumSerializer
from .serializers import CustomUserSerializer

from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model 

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str 
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse



#main page
def show(request):
    return render (request,'index.html')



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

#login

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  
        return render(request, 'login.html', {'form': form})
    

from django.shortcuts import redirect
from django.contrib.auth import logout

def custom_logout(request):
    logout(request)  
    return redirect('home')  

#home


def home(request):
    artists = Artist.objects.all()[:5]
    genres = Genre.objects.all()[:2]
    albums = Album.objects.all()[5:]
    playlists = Playlist.objects.prefetch_related('songs',).all()
    songs = Song.objects.all()[:6] 
    new_releases = Song.objects.all().order_by('-release_date')[:4]  

    return render(request, 'home.html', {
        'artists': artists,
        'genres': genres,
        'albums': albums,
        'playlists': playlists,
        'songs': songs,
        'new_releases': new_releases 
    })







def all_genres(request):
   
    genres = Genre.objects.prefetch_related('song_set').all()  
    return render(request, 'all_genres.html', {'genres': genres})


def all_artists(request):
    artists = Artist.objects.all()  
    return render(request, 'all_artists.html', {'artists': artists})
#####




#####

#subscribe

from django.shortcuts import render
from .models import SubscriptionPlan

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()  
    return render(request, 'subscription_plans.html', {'plans': plans})



def subscribe(request):
    plan_id = request.GET.get('plan_id')

    if not plan_id:
        messages.error(request, 'No plan selected.')
        return redirect('subscription_plans')

    try:
        plan = SubscriptionPlan.objects.get(id=plan_id)
    except SubscriptionPlan.DoesNotExist:
        messages.error(request, 'Subscription plan not found.')
        return redirect('home')

    
    existing_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    if existing_subscription:
        messages.error(request, 'You already have an active subscription to a plan.')
        return redirect('home')

    existing_inactive_subscription = UserSubscription.objects.filter(
        user=request.user,
        plan=plan,
        is_active=False
    ).first()

    if existing_inactive_subscription:
        
        existing_inactive_subscription.end_date = timezone.now() + timedelta(days=plan.duration)
        existing_inactive_subscription.save()
        user_subscription = existing_inactive_subscription
    else:
        
        end_date = timezone.now() + timedelta(days=plan.duration)
        user_subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            end_date=end_date,
            is_active=False  
        )

    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': plan.price,
        'item_name': plan.name,
        'invoice': str(uuid.uuid4()),  
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment_successful')}?subscription_id={user_subscription.id}",
        'cancel_url': f"http://{host}{reverse('payment_failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'paypal': paypal_payment,
        'plan': plan,
        'user': request.user,
        'subscription_start_date': timezone.now(),
        'subscription_end_date': user_subscription.end_date,
    }

    return render(request, 'payment.html', context)





def payment_failed(request):
   
    messages.error(request, "Payment was cancelled or failed. Please try again.")
    return render(request, 'payment_failed.html')

    


def payment_successful(request):
  
    subscription = UserSubscription.objects.filter(user=request.user, is_active=False).first()

    if subscription:
       
        subscription.is_active = True
        subscription.save()
        
       
        messages.success(request, "Payment was successful! Your subscription is now active.")
    else:
       
        messages.error(request, "No pending subscription found. Please contact support.")

  
    return render(request, 'payment_successful.html')









# views.py

from .forms import UserProfileForm
from .models import  UserSubscription, SubscriptionPlan


def user_profile(request):
    user_subscriptions = UserSubscription.objects.filter(user=request.user, is_active=True)
    no_active_subscriptions = not user_subscriptions.exists()

    plans = SubscriptionPlan.objects.all()
    bio = request.user.bio if hasattr(request.user, 'bio') else "No bio available"
    profile_picture = request.user.profile_picture if hasattr(request.user, 'profile_picture') else None

    return render(request, 'user_profile.html', {
        'user_subscriptions': user_subscriptions,
        'plans': plans,
        'no_active_subscriptions': no_active_subscriptions,
        'bio': bio,
        'profile_picture': profile_picture,
        
    })


def profile_update(request):
    """Handle the profile update form for bio, profile picture, and name."""
    if request.method == 'POST':
        
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()  
            return redirect('user_profile') 
    else:
        form = UserProfileForm(instance=request.user)  

    return render(request, 'profile_update.html', {'form': form})






from .models import Song

def song_list(request):
    songs = Song.objects.all()  
    return render(request, 'song_list.html', {'songs': songs})






def search(request):
    query = request.GET.get('q', '')
    
    if query:
        artists = Artist.objects.filter(name__icontains=query).prefetch_related('album_set', 'song_set')
        albums = Album.objects.filter(title__icontains=query).select_related('artist').prefetch_related('song_set')
        songs = Song.objects.filter(title__icontains=query).select_related('album', 'artist')
    else:
        artists = Artist.objects.none()
        albums = Album.objects.none()
        songs = Song.objects.none()

        


    return render(request, 'search_results.html', {
        'results': {
            'artists': artists,
            'albums': albums,
            'songs': songs,
        },
        'query': query,
    })






def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    
    is_following = ArtistFollow.objects.filter(user=request.user, artist=artist).exists()
    follower_count = ArtistFollow.objects.filter(artist=artist).count()

    show_full_bio = request.GET.get('show_full_bio') == 'true'

    return render(request, 'artist_detail.html', {
        'artist': artist,
        'is_following': is_following,
        'follower_count': follower_count,
        'show_full_bio': show_full_bio  
    })


@login_required
def follow_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    
    if not ArtistFollow.objects.filter(user=request.user, artist=artist).exists():
        ArtistFollow.objects.create(user=request.user, artist=artist)
    
    return redirect('artist_detail', artist_id=artist.id) 

@login_required
def unfollow_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    
    followed_artist = ArtistFollow.objects.filter(user=request.user, artist=artist).first()
    if followed_artist:
        followed_artist.delete()
    
    return redirect('artist_detail', artist_id=artist.id)  



def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    artist = album.artist  
    return render(request, 'album_detail.html', {'album': album , 'artist': artist})


def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    return render(request, 'playlist_detail.html', {'playlist': playlist})




from .models import Genre, Song

def library_view(request):
    genres = Genre.objects.all()  
    return render(request, 'library.html', {'genres': genres})





def base_view(request):
    genres = Genre.objects.all()  
    return render(request, 'base.html', {'genres': genres})





def song_detail(request, id):
    song = get_object_or_404(Song, id=id)
    playlist = Song.objects.filter(
        Q(artist=song.artist) | Q(genre=song.genre)
    ).exclude(id=song.id)  
    more_songs = Song.objects.filter(genre=song.genre).exclude(id=song.id)[:10]  
    artist = song.artist  

    return render(request, 'song_detail.html', {
        'song': song,
        'playlist': playlist,
        'more_songs': more_songs,
        'artist': artist
        
    })




def about_us(request):
    return render(request, 'aboutus.html')

def pp(request):
    return render(request,'pp.html')




def song_list(request):
    songs = Song.objects.all()
    return render(request, 'song_list.html', {'songs': songs})




def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin) 
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song_list')  
    else:
        form = SongForm()
    return render(request, 'add_song.html', {'form': form})


@login_required
@user_passes_test(is_admin) 
def edit_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('song_list')  
    else:
        form = SongForm(instance=song)
    return render(request, 'edit_song.html', {'form': form, 'song': song})




@login_required
@user_passes_test(is_admin)  
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('album_detail')  
        else:
           
            return render(request, 'add_album.html', {'form': form})  
    else:
        form = AlbumForm() 
    return render(request, 'add_album.html', {'form': form})  


from django.core.paginator import Paginator

def album_list(request):
    albums = Album.objects.all()
    paginator = Paginator(albums, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'album_list.html', {'page_obj': page_obj})




@login_required
def add_favorite_song(request):
    if request.method == "POST":
        song_id = request.POST.get('song')
        song = Song.objects.get(id=song_id)
       
        if not FavoriteSong.objects.filter(user=request.user, song=song).exists():
            FavoriteSong.objects.create(user=request.user, song=song)
        return redirect('user_profile')  
    
@login_required
def add_favorite_album(request):
    if request.method == "POST":
        album_id = request.POST.get('album')
        album = Album.objects.get(id=album_id)
 
        if not FavoriteAlbum.objects.filter(user=request.user, album=album).exists():
            FavoriteAlbum.objects.create(user=request.user, album=album)
        return redirect('user_profile') 



from django.shortcuts import redirect, get_object_or_404
from .models import ArtistFollow, Artist
from django.contrib.auth.decorators import login_required

@login_required
def follow_artist(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    
    
    if not ArtistFollow.objects.filter(user=request.user, artist=artist).exists():
        ArtistFollow.objects.create(user=request.user, artist=artist)
    
    return redirect('user_profile')




from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):

    profile_picture = request.user.profile_picture.url if request.user.profile_picture else None
    
  
    user_favorite_songs = FavoriteSong.objects.filter(user=request.user)
    user_favorite_albums = FavoriteAlbum.objects.filter(user=request.user)

  
    all_songs = Song.objects.all()
    all_albums = Album.objects.all()

  
    followed_artists_list = ArtistFollow.objects.filter(user=request.user)
    followed_artists_count = followed_artists_list.count()

   
    song_form = FavoriteSongForm()  
    album_form = FavoriteAlbumForm()  
    artist_form = ArtistFollowForm() 

    if request.method == 'POST':
        if 'add_favorite_song' in request.POST:
            song_form = FavoriteSongForm(request.POST)
            if song_form.is_valid():
                song = song_form.save(commit=False)
                song.user = request.user
                if not FavoriteSong.objects.filter(user=request.user, song=song.song).exists():
                    song.save()
                    return redirect('user_dashboard')  
                else:
                    messages.error(request, "This song is already in your favorites.")

        elif 'add_favorite_album' in request.POST:
            album_form = FavoriteAlbumForm(request.POST)
            if album_form.is_valid():
                album = album_form.save(commit=False)
                album.user = request.user
                if not FavoriteAlbum.objects.filter(user=request.user, album=album.album).exists():
                    album.save()
                    return redirect('user_dashboard')  
                else:
                    messages.error(request, "This album is already in your favorites.")

        elif 'follow_artist' in request.POST:
            artist_form = ArtistFollowForm(request.POST)
            if artist_form.is_valid():
                artist_follow = artist_form.save(commit=False)
                artist_follow.user = request.user
                if not ArtistFollow.objects.filter(user=request.user, artist=artist_follow.artist).exists():
                    artist_follow.save()
                    return redirect('user_dashboard')  
                else:
                    messages.error(request, "You are already following this artist.")
    
    
    return render(request, 'user_dashboard.html', {
        'profile_picture': profile_picture,
        'user_favorite_songs': user_favorite_songs,
        'user_favorite_albums': user_favorite_albums,
        'all_songs': all_songs,
        'all_albums': all_albums,
        'song_form': song_form,
        'album_form': album_form,
        'artist_form': artist_form,
        'followed_artists_list': followed_artists_list,
        'followed_artists_count': followed_artists_count,
    })



# *******************************************************
# *******************************************************





class CustomUserCrudView(APIView):
    def post(self, request):
      
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
           
            serializer.save()
            return Response({"Success": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SongCrudView(APIView):
   
    def post(self, request):
        song_data = request.data
        serializer = SongSerializer(data=song_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Song is successfully saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    def get(self, request):
        song_id = request.query_params.get('id', None)

        if song_id:
            try:
                song = Song.objects.get(id=song_id)
                serializer = SongSerializer(song)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Song.DoesNotExist:
                return Response({"Error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            songs = Song.objects.all()
            serializer = SongSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    
    def put(self, request):
        song_id = request.data.get('id', None)
        if not song_id:
            return Response({"Error": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"Error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SongSerializer(song, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Song updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
    def delete(self, request):
        song_id = request.data.get('id', None)
        if not song_id:
            return Response({"Error": "ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            song = Song.objects.get(id=song_id)
            song.delete()
            return Response({"Success": "Song deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Song.DoesNotExist:
            return Response({"Error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)


class ArtistCrudView(APIView):
    def post(self, request):
        artist_data = request.data
        serializer = ArtistSerializer(data=artist_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Artist saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        artist_id = request.query_params.get('id', None)
        if artist_id:
            try:
                artist = Artist.objects.get(id=artist_id)
                serializer = ArtistSerializer(artist)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Artist.DoesNotExist:
                return Response({"Error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            artists = Artist.objects.all()
            serializer = ArtistSerializer(artists, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GenreCrudView(APIView):
    def post(self, request):
        genre_data = request.data
        serializer = GenreSerializer(data=genre_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Genre created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AlbumCrudView(APIView):
    def post(self, request):
        album_data = request.data
        serializer = AlbumSerializer(data=album_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success": "Album created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        User = get_user_model()  
        user = User.objects.filter(email=email).first()
        
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')
            
            send_mail(
                'Password Reset',
                f'Click the link to reset your password: {reset_url}',
                'ashutoshxoxo@gmail.com',  
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'forgot_password.html')

    return render(request, 'forgot_password.html')




def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)

                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('passwordresetdone')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})

def password_reset_done(request):
    return render(request, 'password_reset_done.html')
#****************************************************************************************************
