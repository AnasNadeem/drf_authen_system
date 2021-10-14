from rest_framework import generics, status
from authentication.serializers import (RegisterSerializer,EmailVerificationSerializer)
from rest_framework.response import Response
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.object.get(username=user_data['username'])
        token = RefreshToken.for_user(user).access_token

        cur_site = get_current_site(request).domain
        relative_link = reverse('verify-email')
        abs_url = f"http://{cur_site}{relative_link}?token={token}"

        email_body = f"Hi {user.username} \n Kindly verify your email by clicking the link below \n {abs_url}"
        data = {'email_subject':'Verify your email.', 'email_body':email_body, 'to_email':user.email}
        Util.send_mail(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
  serializer_class = EmailVerificationSerializer
  token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

  @swagger_auto_schema(manual_parameters=[token_param_config])
  def get(self, request):
    token = request.GET.get('token')

    try:
      payload = jwt.decode(token, settings.SECRET_KEY)
      user = User.object.get(id=payload['user_id'])
      if not user.is_verfied:
        user.is_verified = True
        user.save()
      return Response({'email':'Successfully activated'}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
      return Response({'error':"Token has been expired."}, status=status.HTTP_400_BAD_REQUEST)

    except jwt.exceptions.DecodeError:
      return Response({'error':"Invalid Token."}, status=status.HTTP_400_BAD_REQUEST)