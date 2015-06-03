from rest_framework import viewsets

from manager import models
from manager import serializers


class PlayerCharacterViewSet(viewsets.ModelViewSet):
    queryset = models.PlayerCharacter.objects.all()
    serializer_class = serializers.PlayerCharacterSerializer


class NPCTemplateViewSet(viewsets.ModelViewSet):
    queryset = models.NPCTemplate.objects.all()
    serializer_class = serializers.NPCTemplateSerializer


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer


class EncounterNPCViewSet(viewsets.ModelViewSet):
    queryset = models.EncounterNPC.objects.all()
    serializer_class = serializers.EncounterNPCSerializer
