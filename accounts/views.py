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

    def get(self, request, pk=None):
        try:
            user_id = pk or request.query_params.get("id") or request.query_params.get("user_id")
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    return Response(
                        {
                            "success": True,
                            "user": {
                                "id": user.id,
                                "username": user.username,
                                "email": user.email,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                                "phone": user.phone,
                            }
                        },
                        status=status.HTTP_200_OK
                    )
                except User.DoesNotExist:
                    return Response(
                        {
                            "success": False,
                            "message": "User not found"
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            users = User.objects.all()
            user_list = [
                {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": user.phone,
                }
                for user in users
            ]
            return Response(
                {
                    "success": True,
                    "users": user_list
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request):
        try:
            data = request.data
            username = data.get("username")
            email = data.get("email")
            mobileno = data.get("mobileno") or data.get("phone")
            first_name = data.get("first_name")
            last_name = data.get("last_name")

            user = User.objects.create(
                username=username,
                email=email,
                phone=mobileno,
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
                        "phone": user.phone,
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

    def put(self, request, pk=None):
        try:
            data = request.data
            user_id = pk or data.get("id") or data.get("user_id")

            if not user_id:
                return Response(
                    {
                        "success": False,
                        "message": "User ID is required for update"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "User not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            if "username" in data and data["username"] is not None:
                user.username = data["username"]
            if "email" in data and data["email"] is not None:
                user.email = data["email"]
            if "mobileno" in data or "phone" in data:
                user.phone = data.get("mobileno", data.get("phone"))
            if "first_name" in data and data["first_name"] is not None:
                user.first_name = data["first_name"]
            if "last_name" in data and data["last_name"] is not None:
                user.last_name = data["last_name"]

            user.save()

            return Response(
                {
                    "success": True,
                    "message": "User updated successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "phone": user.phone,
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk=None):
        try:
            data = request.data if isinstance(request.data, dict) else {}
            user_id = pk or data.get("id") or data.get("user_id") or request.query_params.get("id") or request.query_params.get("user_id")

            if not user_id:
                return Response(
                    {
                        "success": False,
                        "message": "User ID is required for deletion"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": "User not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            user.delete()

            return Response(
                {
                    "success": True,
                    "message": "User deleted successfully"
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


