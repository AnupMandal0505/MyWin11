from django.shortcuts import render,redirect
from django.views import View
from app.models import User,Location
import random
# from django.http import JsonResponse, HttpResponse

from datetime import datetime

from rest_framework import status

from django.contrib.auth.hashers import make_password

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

# from app.serializers.userSerializer import UserSerializer

from django.core.mail import send_mail,EmailMultiAlternatives
# from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

        
def unique_number(ref):
    name=ref
    while(True):  
        uq=random.randint(1000,9999)
        uq=name+str(uq)
        try:
            # if 'WC' == ref:
            #     n=WasteCollector.objects.get(waste_collector_id=uq)
            # elif 'DWC' == ref : 
            #     n=DistrictWasteCollector.objects.get(district_waste_collector_id=uq)
            # elif 'SWC' == ref :
            #     n=StateWasteCollector.objects.get(state_waste_collector_id=uq)
            # else :
            #     n=User.objects.get(user_id=uq)

            n=Location.objects.get(location_id=uq)

        except:
            return uq
        


class RegisterAPI(APIView):
    def post(self, request):
        try:
            # Extract common user information
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            email = request.data.get('email')
            phone = request.data.get('phone')
            gender = request.data.get('gender','None')

            try:
                user=User.objects.get(phone=phone)
                return Response({"message":'Already Register !'},status=status.HTTP_400_BAD_REQUEST)
            except:

                try:
                    user_type = request.data.get('user_type')
                    password = make_password(phone)

                    if request.data.get('user_type') == 'doctor':
                        location_id = unique_number("loc")
                        address = request.data.get('address')
                        district = request.data.get('district')
                        pincode = request.data.get('pincode')
                        state = request.data.get('state')
                        country = request.data.get('country')
                        locality = request.data.get('locality')

                        return self.register_doctor(request, phone, email, password, first_name, last_name,gender,user_type,location_id,address,district,pincode,state,country,locality)

                    elif user_type == 'technical':
                        return self.register_technical(request, phone, email, password, first_name, last_name,gender,user_type)

                    elif user_type == 'user':
                        return self.register_user(request, phone, email, password, first_name, last_name,gender,user_type)
                except:
                    password = request.data.get('password')
                    return self.register_user(request, phone, email, password, first_name, last_name,gender,user_type="User")
        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)
        



    def register_doctor(self,request, phone, email, password, first_name, last_name,gender,user_type,location_id,address,district,pincode,state,country,locality):
        try:
            user_ref= User.objects.create(phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type=user_type,gender=gender)  
            loc=Location.objects.create(user_ref=user_ref,location_id=location_id,address=address,district=district,pincode=pincode,state=state,country=country,lattitude="lattitude",longitude="longitude",locality=locality)   
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type DOCTOR Section',
                'data': {}
            }
            return Response(error_response, status=400)
        
    def register_technical(self, request, phone, email, password, first_name, last_name,gender,user_type):
        try:
           
            user= User.objects.create(phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type=user_type,gender=gender)       
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type TECHNICAL Section',
                'data': {}
            }
            return Response(error_response, status=400)


    def register_user(self,request, phone, email, password, first_name, last_name,gender,user_type):
        try:
            user= User.objects.create(phone=phone, email=email, password=password, first_name=first_name, last_name=last_name, user_type=user_type,gender=gender)       
            return Response({"message": 'saved Successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'User Type USER Section',
                'data': {}
            }
            return Response(error_response, status=400)
