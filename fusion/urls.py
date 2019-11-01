from django.urls import path
from . import views
from .views import SearchResultsView, AlbumsView

urlpatterns = [
    path('', views.index, name='index'),
    path('songs/',views.songs,name='songs'),
    path('albums/', AlbumsView.as_view(),name='albums'),
    path('listeners/', views.listeners, name='listeners'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
