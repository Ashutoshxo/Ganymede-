from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Genre, Artist, Album, Song, SubscriptionPlan, UserSubscription, Playlist
from django.contrib import admin
from .models import CustomUser, FavoriteSong, FavoriteAlbum, ArtistFollow

class CustomUserAdmin(admin.ModelAdmin):
   
    list_display = ('username', 'email', 'first_name', 'last_name',  'profile_picture', 'is_staff')

   
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password',)
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name',  'profile_picture')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser',)
        }),
    )

    list_editable = [ 'profile_picture']

admin.site.register(CustomUser, CustomUserAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'biography', 'image')
    search_fields = ('name',)

admin.site.register(Artist, ArtistAdmin)

class SongInline(admin.TabularInline):
    model = Album.songs.through  
    extra = 1  


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'cover_image')
    list_filter = ('artist', 'release_date')
    search_fields = ('title', 'artist__name')
    inlines = [SongInline]  

admin.site.register(Album, AlbumAdmin)


class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'duration', 'created_at')
    list_filter = ('genre', 'artist', 'album')
    search_fields = ('title', 'artist__name', 'album__title')

admin.site.register(Song, SongAdmin)


class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'duration')
    search_fields = ('name',)
    list_filter = ('duration',)

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)


class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('user__username', 'plan__name')

admin.site.register(UserSubscription, UserSubscriptionAdmin)

from django.contrib import admin
from .models import Playlist

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'cover_image')  # Display the fields
    search_fields = ('name',)
    filter_horizontal = ('songs',)
admin.site.register(Playlist)



class FavoriteSongAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'added_at')
    search_fields = ('user__username', 'song__title')
    list_filter = ('added_at', 'user')
    ordering = ['-added_at']

admin.site.register(FavoriteSong, FavoriteSongAdmin)

class FavoriteAlbumAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'added_at')
    search_fields = ('user__username', 'album__title')
    list_filter = ('added_at', 'user')
    ordering = ['-added_at']

admin.site.register(FavoriteAlbum, FavoriteAlbumAdmin)

class ArtistFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'artist', 'followed_at')
    search_fields = ('user__username', 'artist__name')
    list_filter = ('followed_at', 'user')
    ordering = ['-followed_at']

admin.site.register(ArtistFollow, ArtistFollowAdmin)






