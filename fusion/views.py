from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
import mysql.connector


#------ Helper function  --------#

def getCursor():
    cnx = mysql.connector.connect(user='aak6sk', password='vahZee6n', host='cs4750.cs.virginia.edu', database='aak6sk')
    return cnx.cursor(), cnx

#------- Views -----#

def index(request):
    # if request.method == 'POST':
    #     if "song-click" in request.POST:
    #         return HttpResponseRedirect('/songs/')
    return render(request, "fusion/index.html")
    #return HttpResponse("Hello, world. You're at the fusion index.")    



class SongsView(TemplateView):
    template_name = 'fusion/songs.html'

class SongSearchView(ListView):
    template_name = 'fusion/song_search.html'

    def get_queryset(self):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        #TODO: Replace 'Album' with 'Song'. It appears that the table 'Song' does not exist yet.
        mycursor.execute("SELECT * FROM Album WHERE name LIKE %s", ("%" + query + "%",))
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
        mycursor.execute("SELECT * FROM Album WHERE name LIKE %s", ("%" + query + "%",))
        album_list=[]
        for item in mycursor:
            album_list.append(item)
        mycursor.close()
        cnx.close()
        return album_list

def listeners(request):
    mycursor, cnx = getCursor()
    mycursor.execute("INSERT INTO Album(album_id, genre, year, name) VALUES(%s,%s,%s,%s)", ('21', 'Hip Hop', '2015', 'City Girlsss'))
    cnx.commit()
    mycursor.execute("SELECT * FROM Album")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)
    cnx.close()
    return render(request, 'fusion/listeners.html', {'listener_list': listener_list})

