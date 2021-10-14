from django.urls import path
from authentication.views import RegisterView, VerifyEmail
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),

]