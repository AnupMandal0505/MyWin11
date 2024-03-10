from django.shortcuts import render,redirect
from django.views import View
from app.models import User,Appointment
import random
# from django.http import JsonResponse, HttpResponse

from datetime import datetime

from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from app.serializers.AppointmentSerializer import AppointmentSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

import json
from urllib.parse import unquote

        
def appointment_unique_number(name):
    name=name
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            n=Appointment.objects.get(appointment_id=uq)
        except:
            return uq
        

@permission_classes([IsAuthenticated]) 
class AppointmentAPI(APIView):
    def post(self, request):
        try:
            print(1)
            date=request.data.get('date')
            print(2)
            slot_time=request.data.get('time')
            age=request.data.get('age')
            weight=request.data.get('weight')
            gender=request.data.get('gender')
            blood_group=request.data.get('blood_group')
            contact=request.data.get('contact')
            patient_name=request.data.get('name')
            relation=request.data.get('relation')
            symptoms=request.data.get('symptoms')
            consultation=request.data.get('consultation')
            # ran = random.randint(999,9999)
            doctor=request.data.get('doctor')
            doctor=User.objects.get(phone=doctor)
            appointment_ref=request.user
            appointment_id=appointment_unique_number("appoint")
            print(12)

            if 'predicted_file' in request.FILES:
          
                predicted_file = request.FILES['predicted_file']
                # result = cloudinary.uploader.upload(predicted_file, folder='MedX/predicted_file')
                result=[]
                url_cloudinary = result['url']
                return self.Appointment(request,appointment_ref,appointment_id,date,slot_time,patient_name,contact,relation,age,weight,blood_group,gender,doctor,consultation,symptoms,url_cloudinary=url_cloudinary)        
            else:
                 return self.Appointment(request,appointment_ref,appointment_id,date,slot_time,patient_name,contact,relation,age,weight,blood_group,gender,doctor,consultation,symptoms)        


        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        



    def Appointment(self,request,appointment_ref,appointment_id,date,slot_time,patient_name,contact,relation,age,weight,blood_group,gender,doctor,consultation,symptoms):
        try:
            df=Appointment.objects.create(appointment_ref=appointment_ref,appointment_id=appointment_id,date=date,slot_time=slot_time,patient_name=patient_name,contact=contact,relation=relation,age=age,weight=weight,blood_group=blood_group,gender=gender,doctor=doctor,consultation=consultation,symptoms=symptoms)        
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Appointment Section',
                'data': {}
            }
            return Response(error_response, status=400)
        
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_history(request):
    try:
        user= request.user
        if user.user_type=='doctor':
            print(45)
            ap = Appointment.objects.filter(doctor=user) 
            print(ap)
            print(3)
            serializer = AppointmentSerializer(ap,many= True)
            return Response({"user":serializer.data})
        elif user.user_type=='user':
            print(45)
            ap = Appointment.objects.filter(appointment_ref=user)
            print(ap)
            print(3)
            serializer = AppointmentSerializer(ap,many= True)
            return Response({"user":serializer.data})
    except Exception as e:
        print("GetUser ERR",e)
        return Response({"messages":"Error"},status=500)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appointment_all(request):
  
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
            ap = Appointment.objects.filter(**DOCTOR,**decoded_filter) 
            print(ap)
            print(3)
            serializer = AppointmentSerializer(ap,many= True)
            return Response({"user":serializer.data})

        elif request.user.user_type == "user":
            print(5454)
            # UserSerializer with ListSerializer
            user_list = Appointment.objects.filter(**USER,**decoded_filter)
            print("kjh",user_list)
            Userdata = AppointmentSerializer(user_list, many=True)
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
