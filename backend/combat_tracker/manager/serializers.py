from rest_framework import serializers

from manager import models


class PlayerCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlayerCharacter


class NPCTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NPCTemplate


class EncounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Encounter


class EncounterNPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EncounterNPC
