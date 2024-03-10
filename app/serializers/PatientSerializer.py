from rest_framework.serializers import ModelSerializer
from app.models import User,Patient
from rest_framework import serializers

class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['rx']


