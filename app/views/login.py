from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers.LoginSerializer import LoginSerializer
from app.serializers.UserSerializer import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginAPI(APIView):

    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            print("before print")
            if serializer.is_valid():
                phone = serializer.data['phone']
                password = serializer.data['password']
                print("After validation print")

                user = authenticate(phone=phone, password=password)
                print("USER DATA",user)
                if user is None:
                    error_response = {
                        'status': 400,
                        'error': 'invalid_password',
                        'message': 'Invalid password',
                        'data': {}
                    }
                    return Response(error_response, status=400)
                print(12)
                refresh = RefreshToken.for_user(user)
                print("After Refress")
                success_response = {
                    'user': UserSerializer(user, many=False).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(success_response)

            else:
                error_response = {
                    'status': 400,
                    'error': 'invalid_data',
                    'message': 'Invalid data',
                    'data': {}
                }
                return Response(error_response, status=400)

        except Exception as e:
            print(e)
            error_response = {
                'status': 400,
                'error': 'something_went_wrong',
                'message': 'Something went wrong',
                'data': {}
            }
            return Response(error_response, status=400)