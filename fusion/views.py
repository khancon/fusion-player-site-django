from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from .forms import NameForm
import mysql.connector
import datetime
from django.contrib.auth.models import User
import json
import csv


#------ Helper function  --------#

def getCursor():
    cnx = mysql.connector.connect(user='dc3jr', password='applesandoranges', host='cs4750.cs.virginia.edu', database='dc3jr')
    return cnx.cursor(), cnx

#------- Views -----#

class IndexView(View):
    # template_name = 'fusion/index.html'
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        users = User.objects.all()
        mycursor.execute("SELECT * FROM listener")
        username_list = []
        for item in mycursor:
            username_list.append(item[0].upper())
        
        print(username_list)
        for user in users:
            if user.username.upper() not in username_list:
                mycursor.execute("INSERT INTO listener(username, password) VALUES (%s,%s)", (user.username, user.password))
                cnx.commit()

        mycursor.close()
        cnx.close()
        context = {}
        return render(request, "fusion/index.html", context)


class WelcomePageView(TemplateView):
    template_name= 'fusion/welcome.html'

class SongsView(TemplateView):
    template_name = 'fusion/songs.html'

class SongSearchView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        playlist_id = self.request.GET.get('playlist_id')
        mycursor.execute("SELECT * FROM song JOIN album USING (album_id) WHERE s_name LIKE %s", ("%" + query + "%",))
        song_list=[]
        for item in mycursor:
            song_list.append(item)
        mycursor.close()
        cnx.close()
        context = {}
        context['object_list'] = song_list
        context['playlist_id'] = playlist_id
        return render(request, 'fusion/song_search.html', context)

class AlbumsView(TemplateView):
    template_name = 'fusion/albums.html'

class ArtistsView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        mycursor.execute("SELECT DISTINCT * FROM artist")
        artist_list=[]
        for item in mycursor:
            artist_list.append(item)
        mycursor.close()
        cnx.close()
        context={}
        context['obj_list'] = artist_list
        return render(request, 'fusion/artists.html', context)

class AlbumSearchView(ListView):
    template_name = 'fusion/album_search.html'

    def get_queryset(self):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        mycursor.execute("SELECT * FROM album WHERE name LIKE %s", ("%" + query + "%",))
        album_list=[]
        for item in mycursor:
            album_list.append(item)
        mycursor.close()
        cnx.close()
        return album_list

class PlaylistsView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        username = self.request.user
        if username != 'AnonymousUser':
            mycursor.execute("SELECT * FROM playlist WHERE username = %s", (str(username),))
        
        my_playlists=[]
        for item in mycursor:
            my_playlists.append(item)

        mycursor.close()
        cnx.close()
        context = {}
        context['my_playlists'] = my_playlists
        context['form'] = NameForm
        return render(request, 'fusion/playlists.html', context)

    def post(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        username = str(self.request.user)
        query = self.request.POST['name']
        time = datetime.datetime.now().replace(microsecond=0).isoformat()
        if username != 'AnonymousUser':
            mycursor.execute("INSERT INTO playlist(username, name,time_created) VALUES(%s,%s,%s)", (username,query,time))
            cnx.commit()
        mycursor.close()
        cnx.close()
        return redirect('/playlists/')

class PlaylistDetailView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        username = self.request.user
        playlist_id = kwargs['playlist_id']
        if playlist_id != None:
            mycursor.execute("SELECT * FROM playlist WHERE playlist_id = %s", (playlist_id,))

        playlist = "404"
        for item in mycursor:
            playlist = item

        mycursor.close()
        cnx.close()
        context = {}
        context['playlist'] = playlist
        context['is_owner'] = (self.request.user.username == playlist[0])
        return render(request, 'fusion/playlist.html', context)

class AlbumDetailView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        username = self.request.user
        album_id = kwargs['album_id']
        if album_id != None:
            mycursor.execute("SELECT * FROM album NATURAL JOIN song WHERE album_id = %s", (album_id,))

        albums = []
        for item in mycursor:
            albums.append(item)

        mycursor.close()
        cnx.close()
        context = {}
        context['albums'] = albums
        return render(request, 'fusion/album.html', context)

class InfoPageView(View):
    def get(self, request, *args, **kwargs):
        mycursor, cnx = getCursor()
        mycursor.execute("SELECT DISTINCT * FROM `playlist` NATURAL JOIN `containing` NATURAL JOIN `song` ORDER BY name")
        song_list=[]
        for item in mycursor:
            song_list.append(item)
        mycursor.close()
        cnx.close()
        context = {}
        context['object_list'] = song_list

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="playlist_containing_song.csv"'

        writer = csv.writer(response)
        
        writer.writerow(['song_id','playlist_id','username','name','time_created','album_id','#_streams','length','sname'])
        for item in song_list:
            writer.writerow(item)

        return response
        #return render(request, "fusion/info.html", context)

class PlaylistSearchView(ListView):
    template_name = 'fusion/playlist_search.html'

    def get_queryset(self):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        mycursor.execute("SELECT * FROM playlist WHERE name LIKE %s", ("%" + query + "%",))
        playlist_list=[]
        for item in mycursor:
            playlist_list.append(item)
        mycursor.close()
        cnx.close()
        return playlist_list

class PlaylistSongsView(View):
    def get(self, request, *args, **kwargs):
        playlist_id = request.GET.get('playlist_id')
        if playlist_id is None:
            playlist_id = kwargs['playlist_id']
        mycursor, cnx = getCursor()
        mycursor.execute("SELECT DISTINCT * FROM containing NATURAL JOIN song NATURAL JOIN album WHERE playlist_id = %s", (playlist_id,))
        song_list=[]
        for item in mycursor:
            song_list.append(item)
        mycursor.execute("SELECT * FROM playlist WHERE playlist_id = %s", (playlist_id,))
        playlist_creator = None
        for item in mycursor:
            playlist_creator = str(item[0])
        is_owner = (playlist_creator == request.user.username)
        mycursor.close()
        cnx.close()
        context = {}
        context['object_list'] = song_list
        context['playlist_id'] = playlist_id
        context['is_owner'] = is_owner
        return render(request, 'fusion/playlist_songs.html', context)

    def post(self, request, *args, **kwargs):
        song_id = self.request.POST['song_id']
        playlist_id = self.request.POST['playlist_id']
        mycursor, cnx = getCursor()
        mycursor.execute("INSERT INTO containing (playlist_id, song_id) VALUES(%s,%s)", (playlist_id, song_id))
        cnx.commit()
        mycursor.close()
        cnx.close()
        return PlaylistSongsView.get(self, request, playlist_id=playlist_id)

    def delete(self, request, *args, **kwargs):
        data = str(request.body)
        song_id_index = data.index('song_id=') + 8
        end_of_song_id = data.index('&',song_id_index)
        playlist_id_index = data.index('playlist_id=') + 12
        end_of_playlist_id = data.index('&',playlist_id_index)
        song_id = int(data[song_id_index:end_of_song_id])
        playlist_id = int(data[playlist_id_index:end_of_playlist_id])
        mycursor, cnx = getCursor()
        mycursor.execute("DELETE FROM containing WHERE playlist_id = %s and song_id = %s", (playlist_id, song_id))
        cnx.commit()
        mycursor.close()
        cnx.close()
        return PlaylistSongsView.get(self, request, playlist_id=playlist_id)

def listeners(request):
    mycursor, cnx = getCursor()
    # mycursor.execute("INSERT INTO Album(album_id, genre, year, name) VALUES(%s,%s,%s,%s)", ('21', 'Hip Hop', '2015', 'City Girlsss'))
    # cnx.commit()
    mycursor.execute("SELECT * FROM listener")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)

    #mycursor.execute("SELECT * FROM listener")


    mycursor.close()
    cnx.close()
    context = {}
    context['listener_list'] = listener_list
    context['friends_list'] = listener_list
    return render(request, 'fusion/listeners.html', context)

class ListenerDetailView(View):
    def get(self, request, *args, **kwargs):
        listener_username = kwargs['listener_username']
        mycursor, cnx = getCursor()
        if listener_username != None:
            mycursor.execute("SELECT * FROM listener WHERE username = %s", (listener_username,))

        listener = None
        for item in mycursor:
            listener = item

        if listener != 'AnonymousUser':
            mycursor.execute("SELECT * FROM playlist WHERE username = %s", (listener[0],))
        
        my_playlists=[]
        for item in mycursor:
            my_playlists.append(item)

        mycursor.close()
        cnx.close()
        context = {}
        context['listener'] = listener[0]
        context['current_user'] = str(self.request.user)
        context['my_playlists'] = my_playlists
        return render(request, 'fusion/listener.html', context)

class FriendsView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("got friend")

    def post(self, request, *args, **kwargs):
        current_user = self.request.POST['current_user']
        listener = self.request.POST['listener']
        date = datetime.datetime.now().replace(microsecond=0).isoformat()
        mycursor, cnx = getCursor()
        mycursor.execute("INSERT INTO friends_with (listener_username, friend_username, starting_date) VALUES(%s,%s, %s)", (current_user, listener, date))
        cnx.commit()
        mycursor.close()
        cnx.close()
        return HttpResponse(listener + " added as a friend")
