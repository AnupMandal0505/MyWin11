from rest_framework.serializers import ModelSerializer
from app.models import Appointment
from rest_framework import serializers

class AppointmentSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        # exclude = ['password']
        fields="__all__"

