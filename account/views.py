from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerialiser,UserProfileSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from .permissions import IsTeamLead,IsOrAdmin,IsEmployee,IsHr,IsAccountent
from attendance.services import get_organisation
from .models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .util import reset_token
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password



# from models import User

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        serialiser=LoginSerialiser(data=request.data)
        
        if serialiser.is_valid():
            user=serialiser.validated_data['user']
            if user.user_type != "SUPER_ADMIN":
                org = get_organisation(user)
                if org and not org.is_active:
                    return Response(
                        {"error": "Organisation is blocked"},
                        status=403
                    )
            token,_=Token.objects.get_or_create(user=user)
            
            return Response({"token":token.key,"user_type":user.user_type,"email":user.email,"id":user.id},status=status.HTTP_201_CREATED)
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)
    
class OrAdminDashboardAPIView(APIView):
    permission_classes = [IsOrAdmin]

    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

class TeamLeadAPIView(APIView):
    permission_classes = [IsTeamLead]
    
    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

class EmployeeAPIView(APIView):
    permission_classes = [IsEmployee]
    
    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)

class HrAPIView(APIView):
    permission_classes = [IsHr]
    
    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)
    
class AccountentAPIView(APIView):
    permission_classes = [IsAccountent]
    
    def get(self, request):
        serializer = UserProfileSerializer(
            request.user,
            context={"request": request}
        )
        return Response(serializer.data)
    
class LogoutAPIView(APIView):

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass

        return Response({"message": "Logout successful"})
    
    
    
# FORGOT PASSWORD


class ForgotPasswordAPI(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        email = request.data.get("email")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=400)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = reset_token.make_token(user)
        
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}/"
        send_mail(
            "Reset your password",
            f"Click link to reset password:\n{reset_link}",
            None,
            [email],
        )

        return Response({"message": "Reset link sent to email"})
    
    
class ResetPasswordAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except:
            return Response({"error": "Invalid link"}, status=400)
        
        if not reset_token.check_token(user, token):
            return Response({"error": "Token expired"}, status=400)

        password = request.data.get("password")

        if not password:
            return Response({"error": "Password required"}, status=400)

        user.password = make_password(password)
        user.save()

        return Response({"message": "Password reset success"})