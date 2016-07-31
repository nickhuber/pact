from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from manager import models
from manager import serializers


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('is_player', )
    ordering_fields = ('name', )
    ordering = ('name', )


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('id', )
    ordering = ('id', )

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
