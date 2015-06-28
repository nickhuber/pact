from rest_framework import serializers

from manager import models


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Character


class EncounterCharacterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    hit_dice = serializers.SerializerMethodField()
    is_player = serializers.SerializerMethodField()

    class Meta:
        model = models.EncounterCharacter

    def get_name(self, obj):
        return obj.character.name

    def get_description(self, obj):
        return obj.character.description

    def get_hit_dice(self, obj):
        return obj.character.hit_dice

    def get_is_player(self, obj):
        return obj.character.is_player


class EncounterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    characters = EncounterCharacterSerializer(source='encountercharacter_set', many=True, required=False)

    class Meta:
        model = models.Encounter
        depth = 1
