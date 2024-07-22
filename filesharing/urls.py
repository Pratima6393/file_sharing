from django.urls import path
from .views import SignUpView, VerifyEmailView, CustomAuthToken, FileUploadView, FileListView, FileDownloadView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('upload-file/', FileUploadView.as_view(), name='upload-file'),
    path('list-files/', FileListView.as_view(), name='list-files'),
    path('download-file/<int:file_id>/', FileDownloadView.as_view(), name='download-file'),
    
    
]
