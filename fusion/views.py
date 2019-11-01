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
    mycursor.execute("SELECT * FROM Listener")
    listener_list=[]
    for item in mycursor:
        listener_list.append(item)

    return render(request, 'fusion/listeners.html', {'listener_list':listener_list})
