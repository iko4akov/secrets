from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.tasks import send_notification
from users.models import User
from users.serializers import UserSerializer, UserRegistrationSerializer
from users.service import generate_token


class UsersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UsersRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def send_verification_email(self, user):
        token = generate_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        mail_subject = 'Подтверждение электронной почты'

        message = render_to_string(
            'users/registrations/verification_email.html',
            {
                'user': user,
                'uid': uid,
                'domain': current_site.domain,
                'token': token
            }
        )

        send_notification.delay(user.email, message, mail_subject)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_verification_email(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UsersVerifyEmailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except Exception as e:
            print(e)
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_verified = True
            user.is_active = True
            user.save()

            return Response(
                data={
                    'message': 'Email is now verified. '
                               'Your account is activated.'
                },
                status=status.HTTP_200_OK
            )

        return Response(
            data={'message': 'Email is not verified. Something went wrong.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UsersRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class UsersDestroyView(generics.DestroyAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
