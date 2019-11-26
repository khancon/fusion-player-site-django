from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, ListView
import mysql.connector


#------ Helper function  --------#

def getCursor():
    cnx = mysql.connector.connect(user='dc3jr', password='applesandoranges', host='cs4750.cs.virginia.edu', database='dc3jr')
    return cnx.cursor(), cnx

#------- Views -----#

def index(request):
    return HttpResponse("Hello, world. You're at the fusion index.")    

class HomeView(TemplateView):
    template_name = 'fusion/home.html'

class WelcomeView(TemplateView):
    template_name = 'welcome.html'


class SongsView(TemplateView):
    template_name = 'fusion/songs.html'

class SongSearchView(ListView):
    template_name = 'fusion/song_search.html'

    def get_queryset(self):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        mycursor.execute("SELECT * FROM song WHERE name LIKE %s", ("%" + query + "%",))
        song_list=[]
        for item in mycursor:
            song_list.append(item)
        mycursor.close()
        cnx.close()
        return song_list

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

def listeners(request):
    mycursor, cnx = getCursor()
    mycursor.execute("INSERT INTO Album(album_id, genre, year, name) VALUES(%s,%s,%s,%s)", ('20', 'Hip Hop', '2015', 'City Girls'))
    cnx.commit()
    mycursor.execute("SELECT * FROM Album")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)
    cnx.close()
    return render(request, 'fusion/listeners.html', {'listener_list': listener_list})

