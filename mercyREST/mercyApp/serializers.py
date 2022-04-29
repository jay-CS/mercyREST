from rest_framework import serializers
from . models import User,File

class userSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        
class fileSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = File
        fields = "__all__"