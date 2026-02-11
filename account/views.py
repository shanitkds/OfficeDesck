from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerialiser 
from rest_framework.permissions import AllowAny
from rest_framework import status

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self,request):
        serialiser=LoginSerialiser(data=request.data)
        
        if serialiser.is_valid():
            user=serialiser.validated_data['user']
            token,_=Token.objects.get_or_create(user=user)
            
            return Response({"token":token.key,"user_type":user.user_type,"email":user.email})
        return Response(serialiser.errors,status=status.HTTP_400_BAD_REQUEST)