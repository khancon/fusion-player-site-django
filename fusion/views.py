from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
import mysql.connector


#------ Helper function  --------#

def getCursor():
    cnx = mysql.connector.connect(user='aak6sk', password='vahZee6n', host='cs4750.cs.virginia.edu', database='aak6sk')
    return cnx.cursor(), cnx

#------- Views -----#

def index(request):
    return HttpResponse("Hello, world. You're at the fusion index.")

class SearchResultsView(ListView):
    template_name = 'fusion/search_results.html'

    def get_queryset(self):
        mycursor, cnx = getCursor()
        query = self.request.GET.get('q')
        mycursor.execute("SELECT * FROM Album WHERE name LIKE %s", ("%" + query + "%",))
        album_list=[]
        for item in mycursor:
            album_list.append(item)
        print(mycursor)
        mycursor.close()
        cnx.close()
        return album_list

class AlbumsView(TemplateView):
    template_name = 'fusion/albums.html'

def songs(request):
    mycursor, cnx  = getCursor()
    mycursor.execute("SELECT * FROM Album")
    list1=[]
    for item in mycursor:
        list1.append(item[3] + '<br>')
    cnx.close() 
    return HttpResponse(list1)

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

