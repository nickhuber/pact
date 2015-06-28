from rest_framework import viewsets

from manager import models
from manager import serializers


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer


class EncounterCharacterViewSet(viewsets.ModelViewSet):
    queryset = models.EncounterCharacter.objects.all()
    serializer_class = serializers.EncounterCharacterSerializer
