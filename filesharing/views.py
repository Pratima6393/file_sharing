from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import User, File
from .serializers import UserSerializer, FileSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import jwt
import datetime
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.utils.http import int_to_base36
from .permissions import *

@permission_classes([AllowAny])
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, settings.SECRET_KEY, algorithm='HS256')
        verification_url = f"http://localhost:8000/verify-email/?token={token}"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
@permission_classes([AllowAny])
class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id,is_active=True)
        if user:
            
            return Response({'token': token.key, 'user_id': user.pk, 'user_type': user.user_type})
        else:
            return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(generics.CreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated, IsOperationUser]

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        if file:
            # Check if file.name has extension
            if not file.name or not any(file.name.lower().endswith(ext) for ext in ('.pptx', '.docx', '.xlsx','pdf')):
                return Response({'error': 'Only .pptx, .docx, and .xlsx files are allowed.'}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(uploaded_by=self.request.user)
        else:
            return Response({'error': 'No file was uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated,IsClientUser]
    def get(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        try:
            file = File.objects.get(id=file_id)
            if file.uploaded_by.user_type == 'operation':
                # Generate a secure URL for the file
                response_data = {
                    'download-link': request.build_absolute_uri(file.file.url),
                    'message': 'success'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except File.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated,IsClientUser]


    def get_queryset(self):
        return File.objects.all()
    
