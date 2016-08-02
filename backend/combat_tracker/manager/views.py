from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from manager import models
from manager import serializers


class NoListModelViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


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
    ordering_fields = ('name', )
    ordering = ('name', )

    @detail_route(methods=['post'])
    def advance_initiative(self, request, pk=None):
        encounter = self.get_object()
        encounter.advance_initiative()
        serializer = self.get_serializer(instance=encounter)
        return Response(serializer.data)


class EncounterCharacterViewSet(NoListModelViewSet):
    queryset = models.EncounterCharacter.objects.all()
    serializer_class = serializers.EncounterCharacterSerializer


class StatusEffectViewSet(NoListModelViewSet):
    queryset = models.StatusEffect.objects.all()
    serializer_class = serializers.StatusEffectSerializer
