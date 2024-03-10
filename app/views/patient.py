from django.shortcuts import render,redirect
from django.views import View
from app.models import Appointment,Patient
import random
# from django.http import JsonResponse, HttpResponse

from datetime import datetime

from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

# from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from app.serializers.PatientSerializer import PatientSerializer
import json
from urllib.parse import unquote

        
def patient_unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=Patient.objects.get(appointment_id=uq)
        except:
            return uq
        

@permission_classes([IsAuthenticated]) 
class PatientAPI(APIView):
    def post(self, request,slug):
        try:
            symptoms=request.data.get('symptoms')
            suggestion_test=request.data.get('suggestion_test')
            advice=request.data.get('advice')
            rx=request.data.get('rx')
        
            appointment_id = slug
            
            id=Appointment.objects.get(appointment_id=appointment_id)
            print(id)
            try:
                data = Patient.objects.get(patient_ref=id)
                return Response({"message": 'Already Exit'}, status=status.HTTP_208_ALREADY_REPORTED)

            except:
                print(234)
                id.status=True
                id.save()
                patient_id=patient_unique_number("pat")
                ab=Patient.objects.create(patient_ref=id,patient_id=patient_id,symptoms=symptoms,suggestion_test=suggestion_test,advice=advice,rx=rx)
                # b=Payment.objects.create(user=user,payment_ref=ab,amount=500)
                return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response({"message": 'External Problem'}, status=status.HTTP_400_BAD_REQUEST)
        



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_history(request,slug):
    try:
        ap = Patient.objects.get(patient_ref=slug) 
        serializer = PatientSerializer(ap,many= False)
        return Response({"user":serializer.data})
       
    except Exception as e:
        print("GetUser ERR",e)
        return Response({"messages":"Error"},status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_all(request):
  
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
        ResponseData = []
        print(1515)
        USER = {
        "appointment_ref":request.user
        }

        DOCTOR = {
        "doctor":request.user
        }
        
        if request.user.user_type == "doctor":
            # UserSerializer with ListSerializer
            ap = Patient.objects.filter(**decoded_filter) 
            print(ap)
            print(3)
            serializer = PatientSerializer(ap,many= True)
            return Response({"user":serializer.data})

        elif request.user.user_type == "user":
            print(5454)
            # UserSerializer with ListSerializer
            user_list = Patient.objects.filter(**decoded_filter)
            print("kjh",user_list)
            Userdata = PatientSerializer(user_list, many=True)
            ResponseData += list(Userdata.data)

            return ResponseData
        
        else:
            error_response = {
            'status': 500,
            'error': 'Check Filter',
            'message': 'error',
            'data': {}
        }
        return Response(error_response, status=500)


    except Exception as e:
        print("Error", e)
        error_response = {
            'status': 500,
            'error': 'Check Filter',
            'message': 'Internal server error',
            'data': {}
        }
        return Response(error_response, status=500)
