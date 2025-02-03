from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

# Custom User Model
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username

# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Artist Model
class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    biography = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='artist_images/', blank=True, null=True)  

    def __str__(self):
        return self.name

# Song Model
class Song(models.Model):
    title = models.CharField(max_length=200  )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, blank=True, null=True)  
    release_date = models.DateField(blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    music_file = models.FileField(upload_to="music/", blank=True, null=True)
    
    class Meta:
        ordering = ['genre', '-release_date'] 
       
        
    def __str__(self):
        return self.title

# Album Model
class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_date = models.DateField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)
    songs = models.ManyToManyField(Song, related_name='albums', blank=True)

    def __str__(self):
        return self.title

# Subscription Plan Model
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in days")

    def __str__(self):
        return self.name

# User Subscription Model
class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'plan', 'is_active')

# Playlist Model
from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='playlists/', blank=True, null=True)  # New field for image

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


# # Play History Model
# class PlayHistory(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     played_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} played {self.song.title} on {self.played_at}'

# Favorite Song Model
class FavoriteSong(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f'{self.user.username} favorited {self.song.title}'

# Favorite Album Model
class FavoriteAlbum(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'album')

    def __str__(self):
        return f'{self.user.username} favorited {self.album.title}'

# Artist Follow Model
class ArtistFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artist')

    def __str__(self):
        return f'{self.user.username} followed {self.artist.name}'

# # Playlist History Model
# class PlaylistHistory(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     song = models.ForeignKey(Song, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'{self.user.username} added {self.song.title} to {self.playlist.name}'


# class PlaylistCollaborator(models.Model):
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('playlist', 'user')

#     def __str__(self):
#         return f'{self.user.username} is a collaborator on {self.playlist.name}'

# User Profile Model 
# class UserProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     favorite_genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
#     favorite_artists = models.ManyToManyField(Artist, blank=True)
    
    
#     def __str__(self):
#         return f'{self.user.username} Profile'




