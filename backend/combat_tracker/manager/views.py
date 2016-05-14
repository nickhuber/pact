from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from manager import models
from manager import serializers


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer

    @detail_route(methods=['post'])
    def advance_initiative(self, request, pk=None):
        encounter = self.get_object()
        encounter.advance_initiative()
        serializer = self.get_serializer(instance=encounter)
        return Response(serializer.data)


class EncounterCharacterViewSet(viewsets.ModelViewSet):
    queryset = models.EncounterCharacter.objects.all()
    serializer_class = serializers.EncounterCharacterSerializer


class StatusEffectViewSet(viewsets.ModelViewSet):
    queryset = models.StatusEffect.objects.all()
    serializer_class = serializers.StatusEffectSerializer
