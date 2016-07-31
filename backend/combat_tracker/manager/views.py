from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from manager import models
from manager import serializers


class CharacterViewSet(viewsets.ModelViewSet):
    # lookup_field = 'uuid'
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_fields = ('is_player', )
    ordering_fields = ('name', )
    ordering = ('name', )


class EncounterViewSet(viewsets.ModelViewSet):
    # lookup_field = 'uuid'
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('name', )
    ordering = ('name', )

    @detail_route(methods=['post'])
    def advance_initiative(self, request, pk=None):
        encounter = self.get_object()
        encounter.advance_initiative()
        serializer = self.get_serializer(instance=encounter)
        return Response(serializer.data)


class EncounterCharacterViewSet(viewsets.ModelViewSet):
    # lookup_field = 'uuid'
    queryset = models.EncounterCharacter.objects.all()
    serializer_class = serializers.EncounterCharacterSerializer


class StatusEffectViewSet(viewsets.ModelViewSet):
    # lookup_field = 'uuid'
    queryset = models.StatusEffect.objects.all()
    serializer_class = serializers.StatusEffectSerializer
