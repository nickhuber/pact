from rest_framework import serializers

from django.contrib.auth import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'email',)
