from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, View
from .forms import NameForm
import mysql.connector
import datetime
from django.contrib.auth.models import User


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
            username_list.append(item[0])
        
        print(username_list)
        for user in users:
            if user.username not in username_list:
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
            mycursor.execute("INSERT INTO playlist(username, name, time_created) VALUES(%s,%s,%s)", (username,query,time))
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
        return render(request, 'fusion/playlist.html', context)

class InfoPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'fusion/info.html', context)

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

class PlaylistModificationView(View):
    def get(self, request, *args, **kwargs):
        print("HEY, GET")

    def post(self, request, *args, **kwargs):
        print("HEY, POST")

def listeners(request):
    mycursor, cnx = getCursor()
    # mycursor.execute("INSERT INTO Album(album_id, genre, year, name) VALUES(%s,%s,%s,%s)", ('21', 'Hip Hop', '2015', 'City Girlsss'))
    # cnx.commit()
    mycursor.execute("SELECT * FROM listener")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)
    cnx.close()
    return render(request, 'fusion/listeners.html', {'listener_list': listener_list})

