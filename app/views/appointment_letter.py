from django.shortcuts import render,redirect,HttpResponse
import random
# from app.models import Patient,Appointment,Department
from django.contrib import messages
from app.models import User,Appointment

from rest_framework.views import APIView
   
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ListSerializer, ValidationError

from app.serializers.UserSerializer import UserSerializer
from app.serializers.AppointmentSerializer import AppointmentSerializer

import json
from urllib.parse import unquote

# Only Get Appointment
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDetails(request):
    try:
        user= request.user
        serializer = AppointmentSerializer(user,many= False)
        return Response({"user":serializer.data})
    except Exception as e:
        print("GetUser ERR",e)
        return Response({"messages":"Error"},status=500)



def getUserByType(user_ref, filter):

    ResponseData = []

    if user_ref.user_type=="user":
        appointment_ref=Appointment.objects.get(appointment_ref=user_ref)
        appointment_data=AppointmentSerializer(Appointment.objects.filter(**appointment_ref, **filter), many=True)
        ResponseData += appointment_data.data

    elif user_ref.user_type=="doctor":
        appointment_data=AppointmentSerializer(Appointment.objects.filter(**filter), many=True)
        ResponseData += appointment_data.data

    return ResponseData

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserALL(request):
    try:
        # print("params",type(request.query_params.get("name")))
        # Get the encoded filter from the query parameters
        encoded_filter = request.query_params.get('filter', None)
        decoded_filter = {}
        try:
            # Decode and parse the JSON filter
            decoded_filter = json.loads(unquote(encoded_filter))
        except:
            decoded_filter = {}

        print("decoded_filter",decoded_filter)

        # Check if the decoded filter is a dictionary
        if not isinstance(decoded_filter, dict):
            decoded_filter={}

        ResponseData=getUserByType(request.user,decoded_filter)
        return Response(ResponseData)
    
    except Exception as e:
        print("Error", e)
        error_response = {
            'status': 500,
            'error': 'something_went_wrong',
            'message': 'Internal server error',
            'data': {}
        }
        return Response(error_response, status=500)





# @permission_classes([IsAuthenticated]) 
# class GetDistrictWasteCollector(APIView):
#     def get(self, request):
#         try:
#             # print("params",type(request.query_params.get("name")))
#             # Get the encoded filter from the query parameters
#             encoded_filter = request.query_params.get('filter', None)
#             decoded_filter = {}
#             print("1",decoded_filter)
#             try:
#                 # Decode and parse the JSON filter
#                 decoded_filter = json.loads(unquote(encoded_filter))
#                 print("2",decoded_filter)
#             except:
#                 decoded_filter = {}
#                 print("3",decoded_filter)



#             # Check if the decoded filter is a dictionary
#             if not isinstance(decoded_filter, dict):
#                 decoded_filter={}
#                 print("4",decoded_filter)
            
#              # Filter based on the decoded filter
#             data_queryset = DistrictWasteCollector.objects.filter(**decoded_filter)

#             # Serialize the queryset
#             serializer = UserDistrictCollectorSerializer(data=data_queryset, many=True)
#             serializer.is_valid()  # Call .is_valid() before accessing .data
#             serialized_data = serializer.data  # Access the serialized data

#             # Print or do something with the serialized data

#             return Response({"message": serialized_data})
     
#         except Exception as e:
#             print("Error", e)
#             error_response = { 
#                 'status': 500,
#                 'error': 'something_went_wrong',
#                 'message': 'Internal server error',
#                 'data': {}
#             }
#             return Response(error_response, status=500)
    