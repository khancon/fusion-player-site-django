from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

# Create your views here.

cnx = mysql.connector.connect(user='aak6sk', password='vahZee6n', host='cs4750.cs.virginia.edu', database='aak6sk')
mycursor = cnx.cursor()

def index(request):
    return HttpResponse("Hello, world. You're at the fusion index.")

def songs(request):
    mycursor.execute("SELECT * FROM Album")
    list1=[]
    for item in mycursor:
        list1.append(item[3] + '<br>')

    return HttpResponse(list1)

def listeners(request):
    mycursor.execute("INSERT INTO Album(album_id, genre, year, name) VALUES(%s,%s,%s,%s)", ('17', 'EDM', '2015', 'Lights'))
    cnx.commit()
    mycursor.execute("SELECT * FROM Album")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)

    mycursor.close()
    cnx.close()
    #return HttpResponse(listener_list)
    return render(request, 'fusion/listeners.html', {'listener_list': listener_list})
