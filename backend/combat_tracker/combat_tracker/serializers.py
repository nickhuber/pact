from rest_framework import serializers

from django.contrib.auth import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.User
        fields = ('id', 'username', 'email',)
