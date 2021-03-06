from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    # For the signup page
    path('accounts/', include('accounts.urls')),
    # For the signin page
    path('accounts/', include('django.contrib.auth.urls')),
    path('welcome/',WelcomePageView.as_view(),name='welcome'),
    path('', IndexView.as_view(), name='index'),
    path('songs/',SongsView.as_view(),name='songs'),
    path('albums/', AlbumsView.as_view(),name='albums'),
    path('albums/<int:album_id>', AlbumDetailView.as_view(), name='album'),
    path('artists/', ArtistsView.as_view(),name='artists'),
    #path('artist/<int:artist_id>/',ArtistDetailView.as_view(),name='artist'),
    path('playlists/', PlaylistsView.as_view(), name='playlists'),
    path('playlists/<int:playlist_id>/',PlaylistDetailView.as_view(), name='playlist'),
    path('listeners/', views.listeners, name='listeners'), 
    path('listeners/<str:listener_username>/', ListenerDetailView.as_view(), name='listener'),
    path('ajax/song_search/', SongSearchView.as_view(), name='song_search'),
    path('ajax/album_search/', AlbumSearchView.as_view(), name='album_search'),
    path('ajax/playlist_search/', PlaylistSearchView.as_view(), name='playlist_search'),
    path('info/', InfoPageView.as_view(), name="info"),
    path('ajax/playlist_songs/', PlaylistSongsView.as_view(), name='playlist_songs'),
    path('ajax/friends/', FriendsView.as_view(), name='friends'),
    path('ajax/mashup/', MashupView.as_view(), name='mashup'),
    path('by_us/', ByUsView.as_view(), name="by_us")
]