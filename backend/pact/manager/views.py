import django_filters.rest_framework
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from manager import models
from manager import serializers


class NoListModelViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    pass


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = models.Character.objects.all()
    serializer_class = serializers.CharacterSerializer
    filter_fields = ('is_player', )
    ordering_fields = ('name', )
    ordering = ('name', )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EncounterViewSet(viewsets.ModelViewSet):
    queryset = models.Encounter.objects.all()
    serializer_class = serializers.EncounterSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('name', )
    ordering = ('name', )

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created_by=self.request.user)

    @detail_route(methods=['post'])
    def advance_initiative(self, request, pk=None):
        encounter = self.get_object()
        encounter.advance_initiative()
        serializer = self.get_serializer(instance=encounter)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EncounterCharacterViewSet(NoListModelViewSet):
    queryset = models.EncounterCharacter.objects.all()
    serializer_class = serializers.EncounterCharacterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(encounter__created_by=self.request.user)


class StatusEffectViewSet(NoListModelViewSet):
    queryset = models.StatusEffect.objects.all()
    serializer_class = serializers.StatusEffectSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            character__encounter__created_by=self.request.user
        )


class PathfinderMonsterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.PathfinderMonster.objects.all()
    serializer_class = serializers.PathfinderMonsterSerializer

    def get_queryset(self):
        name_search_term = self.request.query_params.get('name_search_term', '')
        # Avoid hitting the database hard and returning huge queries
        if len(name_search_term) < 3:
            return models.PathfinderMonster.objects.none()

        return super().get_queryset().filter(name__icontains=name_search_term)


class FifthEditionMonsterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.FifthEditionMonster.objects.all()
    serializer_class = serializers.FifthEditionMonsterSerializer

    def get_queryset(self):
        name_search_term = self.request.query_params.get('name_search_term', '')
        # Avoid hitting the database hard and returning huge queries
        if len(name_search_term) < 3:
            return models.FifthEditionMonster.objects.none()

        return super().get_queryset().filter(name__icontains=name_search_term)
