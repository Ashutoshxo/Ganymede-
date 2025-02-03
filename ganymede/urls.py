from django.urls import path ,include
from .import views
from .views import register ,LoginView,all_artists, subscribe 
from .views import artist_detail,user_profile,playlist_detail,album_detail
from .views import library_view,search,song_list,song_detail
from .views import SongCrudView,ArtistCrudView,GenreCrudView, AlbumCrudView, CustomUserCrudView


urlpatterns = [
    path('',views.show),
    path("register/", views.register, name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('home/', views.home, name='home'), 
    path('logout/', views.custom_logout, name='logout'), 
    path('artists/', all_artists, name='all_artists'), 
    path('subscribe/', views.subscribe, name='subscribe'),
   
    
    path('profile/', user_profile, name='user_profile'),
    path('add_album/', views.add_album, name='add_album'),
    path('albums/', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    path('library/', views.library_view, name='library'),
    path('search/', search, name='search'),
    path('genres/',views.all_genres,name='all_genres'),
    path('songs/', song_list, name='song_list'),
    path('add-song/', views.add_song, name='add_song'),  
    path('edit-song/<int:song_id>/', views.edit_song, name='edit_song'),  
    path('song/<int:id>/', views.song_detail, name='song_detail'),
    path('aboutus/', views.about_us, name='about_us'),
    path('pp/',views.pp, name='pp'),
    path('subscription-plans/', views.subscription_plans, name='subscription_plans'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('payment-successful/', views.payment_successful, name='payment_successful'),
    path('add_favorite_song/', views.add_favorite_song, name='add_favorite_song'),
    path('add_favorite_album/', views.add_favorite_album, name='add_favorite_album'),
    
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('artist/<int:artist_id>/follow/', views.follow_artist, name='follow_artist'),
    path('artist/<int:artist_id>/unfollow/', views.unfollow_artist, name='unfollow_artist'),

    path('songs/create/', SongCrudView.as_view(), name='song-crud-view'),
    path('artists/crud/', ArtistCrudView.as_view(), name='artist-crud-view'),
    path('genres/crud/', GenreCrudView.as_view(), name='genre-crud-view'),
    path('users/crud/', CustomUserCrudView.as_view(), name='customuser-crud-view'),
    path('albums/crud/', AlbumCrudView.as_view(), name='album-crud-view'),
    ######################################################
    path('forgotpassword/', views.forgot_password, name="forgotpassword"),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),
    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),

    
    
    
    ]
    
    


 


 