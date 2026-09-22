from django.contrib.auth import authenticate

# Create your views here.

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import LoginSerializer, RegisterSerializer, UserSerializer


@extend_schema(request=RegisterSerializer, responses=RegisterSerializer)
class SignupView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(role='user')
        username = serializer.data['username']
        email = serializer.data['email']

        return Response({'user': {'username':username,'email':email},'message':'successfully registered'}, status=status.HTTP_201_CREATED)
@extend_schema(request=LoginSerializer, responses=LoginSerializer)
class Loginview(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usercheck = serializer.validated_data.get('user')
        user = authenticate(username=usercheck.username, password=serializer.validated_data['password'])
        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        response = Response({
            'accesstoken': str(refresh.access_token),
            'name': user.username,
            'role': user.role,
        }, status=status.HTTP_200_OK)
        response.set_cookie('refresh_token', str(refresh),samesite='Lax',httponly=True,secure=False,max_age=60 * 60 * 24 * 7)
        return response


class RefreshTokenView(APIView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get('refresh_token')
        if refresh is None:
            return Response({'error': 'User is not logged in'}, status=status.HTTP_403_FORBIDDEN)
        refreshvval = RefreshToken(refresh)
        newaccess_token = str(refreshvval.access_token)
        user_id = refreshvval.payload['user_id']
        user = User.objects.get(id=user_id)
        return Response({'access_token': newaccess_token, 'username': user.username, 'role': user.role})


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

        except Exception:
            pass

        response = Response({"message": "Logout successful"}, status=200)
        response.delete_cookie( 'refresh_token')
        return response


class ProfileAPIView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)