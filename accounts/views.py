from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import RegisterSerializer



class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "User registered successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class ProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user

        return Response({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        })


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {
                        "success": False,
                        "message": "Refresh token is required"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message": "Successfully logged out"
                },
                status=status.HTTP_200_OK
            )
        except TokenError as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": "An error occurred during logout"
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class saveUser(APIView):
    def post(self,request):
        print("request.data is ",{request.data})
        try:
            data= request.data
            username = data.get("username")
            email = data.get("email")
            mobileno = data.get("mobileno")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            user = User.objects.create(
                username=username,
                email=email,
                mobileno=mobileno,
                first_name=first_name,
                last_name=last_name
            )

            return Response(
                {
                    "success": True,
                    "message": "User saved successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )            

