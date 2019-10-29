from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector

# Create your views here.

cnx = mysql.connector.connect(user='aak6sk', password='vahZee6n', host='cs4750.cs.virginia.edu', database='aak6sk')
mycursor = cnx.cursor()

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def songs(request):
    mycursor.execute("SELECT * FROM Listener")
    return HttpResponse(mycursor)
