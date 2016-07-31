from django.contrib.auth import models, authenticate, login

from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from combat_tracker import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class LoginView(views.APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.UserSerializer

    # TODO: This is probably insecure, there must be a better way
    def post(self, request, *args, **kwargs):
        logged_in = False
        user = authenticate(
            username=request.data['username'],
            password=request.data['password']
        )
        if user is not None:
            login(request, user)
            logged_in = True
        if not logged_in:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.serializer_class(user).data)


class RegisterView(views.APIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        taken_username = models.User.objects.filter(
            username=request.data['username']
        ).exists()
        taken_email = models.User.objects.filter(
            email=request.data['email']
        ).exists()
        if taken_username or taken_email:
            errors = {}
            if taken_email:
                errors['email'] = ['Email already in use']
            if taken_username:
                errors['username'] = ['Username already in use']
            raise ValidationError(errors)
        user = models.User.objects.create_user(
            request.data['username'],
            request.data['email'],
            request.data['password'],
            is_active=False,
        )
        return Response(self.serializer_class(user).data)
