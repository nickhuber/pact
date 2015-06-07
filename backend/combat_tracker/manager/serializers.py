from rest_framework import serializers

from manager import models


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Encounter
        depth = 1


class EncounterCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EncounterCharacter
