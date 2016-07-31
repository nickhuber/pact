from rest_framework import serializers

import dice
from pyparsing import ParseException

from manager import models


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Character
        # extra_kwargs = {
        #     'url': {'lookup_field': 'uuid'}
        # }

    def validate(self, data):
        if not data.get('is_player') and not data.get('hit_dice'):
            raise serializers.ValidationError(
                {'hit_dice': 'Hit dice required for NPCs.'}
            )
        if data.get('is_player') and data.get('hit_dice'):
            raise serializers.ValidationError(
                {'hit_dice': 'Hit dice cannot be used for players.'}
            )
        return data

    def validate_hit_dice(self, value):
        if value is None or value == '':
            return ''
        try:
            # We don't care what we get, just make sure it is valid
            dice.roll(value)
        except (ParseException, KeyError):
            raise serializers.ValidationError('Invalid hit dice')
        return value


class StatusEffectSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.StatusEffect
        # extra_kwargs = {
        #     'url': {'lookup_field': 'uuid'}
        # }
        # exclude = ('character',)


class EncounterCharacterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(
        source='character.name',
        read_only=True
    )
    description = serializers.CharField(
        source='character.description',
        read_only=True
    )
    is_player = serializers.BooleanField(
        source='character.is_player',
        read_only=True
    )
    status_effects = StatusEffectSerializer(
        source='statuseffect_set',
        many=True,
        required=False
    )
    # character = serializers.HyperlinkedIdentityField(
    #     view_name='character-detail',
    #     lookup_field='uuid',
    #     read_only=True
    # )
    # encounter = serializers.HyperlinkedIdentityField(
    #     view_name='encounter-detail',
    #     lookup_field='uuid',
    #     read_only=True
    # )

    class Meta:
        model = models.EncounterCharacter
        # extra_kwargs = {
        #     'url': {'lookup_field': 'uuid'}
        # }


class EncounterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    # characters = serializers.HyperlinkedRelatedField(
    #     source='encountercharacter_set',
    #     view_name='encountercharacter-detail',
    #     read_only=True,
    #     lookup_field='uuid',
    #     many=True,
    #     required=False,
    # )

    class Meta:
        model = models.Encounter
        # extra_kwargs = {
        #     'url': {'lookup_field': 'uuid'}
        # }
        depth = 1
