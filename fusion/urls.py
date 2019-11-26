from django.urls import path
from . import views
from .views import SongsView, SongSearchView,AlbumSearchView, AlbumsView

urlpatterns = [
    #path('welcome/',WelcomePageView.as_view(),name='welcome'),
    #path('create-account/',CreateAccountView.as_view(),name='create-account'),
    #path('sign-in/',SignInView.as_view(),name='sign-in'),
    path('', views.index, name='index'),
    path('songs/',SongsView.as_view(),name='songs'),
    #path('song/<int:song_id>',SongView.as_view(),name='song')
    path('albums/', AlbumsView.as_view(),name='albums'),
    #path('albums/<int:album_id>/', AlbumView.as_view(),name='album'),
    #path('artists/',Artists.as_view(),name='artists'),
    #path('artist/<int:artist_id>/',Artist.as_view(),name='artist'),
    #path('playlists/', PlaylistsView.as_view(), name='playlists'),
    #path('playlists/<int:playlist_id>/',PlaylistsView.as_view(), name='playlist'),
    #path('create-playlist/', CreatePlaylistView.as_view(), name='create-playlist'),
    path('listeners/', views.listeners, name='listeners'), 
    path('ajax/song_search/', SongSearchView.as_view(), name='song_search'),
    path('ajax/album_search/', AlbumSearchView.as_view(), name='album_search'),
]
