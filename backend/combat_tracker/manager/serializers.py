from rest_framework import serializers

import dice
from pyparsing import ParseException

from manager import models


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Character

    def validate(self, data):
        if not data.get('is_player') and not data.get('hit_dice'):
            raise serializers.ValidationError({'hit_dice': 'Hit dice required for NPCs.'})
        if data.get('is_player') and data.get('hit_dice'):
            raise serializers.ValidationError({'hit_dice': 'Hit dice cannot be used for players.'})
        return data

    def validate_hit_dice(self, value):
        if value is None or value == '':
            return ''
        try:
            results = dice.roll(value)
        except (ParseException, KeyError):
            raise serializers.ValidationError('Invalid hit dice')
        return value


class StatusEffectSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.StatusEffect


class EncounterCharacterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source='character.name', read_only=True)
    description = serializers.CharField(source='character.description', read_only=True)
    is_player = serializers.BooleanField(source='character.is_player', read_only=True)
    status_effects = StatusEffectSerializer(source='statuseffect_set', many=True, required=False)

    class Meta:
        model = models.EncounterCharacter


class EncounterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    characters = EncounterCharacterSerializer(source='encountercharacter_set', many=True, required=False)

    class Meta:
        model = models.Encounter
        depth = 1
