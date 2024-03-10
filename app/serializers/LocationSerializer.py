from rest_framework.serializers import ModelSerializer
from app.models import User, Location
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','delete','is_staff','is_superuser','is_active','user_permissions','groups','last_login']



class LocationSerializer(ModelSerializer):
    user = UserSerializer()  
    class Meta:
        model = Location
        exclude = ['address']

