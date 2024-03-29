import math

from rest_framework import serializers

import dice
from pyparsing import ParseException

from manager import models


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    class Meta:
        model = models.Character
        exclude = ('created_by',)

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
        fields = '__all__'


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
        required=False,
        read_only=True,
    )

    def validate(self, data):
        if 'current_hp' in data:
            data['current_hp'] = min(data['current_hp'], self.instance.max_hp)
        return data

    class Meta:
        model = models.EncounterCharacter
        fields = '__all__'


class EncounterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)

    characters = EncounterCharacterSerializer(
        source='encountercharacter_set',
        many=True,
        required=False,
        read_only=True,
    )
    active_character_uuids = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = models.Encounter
        exclude = ('created_by', )
        depth = 1

    def get_active_character_uuids(self, encounter):
        if encounter.current_initiative is None:
            return []
        characters_query = encounter.encountercharacter_set\
            .filter(initiative=encounter.current_initiative)
        return [c.uuid for c in characters_query]


class PathfinderMonsterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    initiative = serializers.SerializerMethodField()
    perception = serializers.SerializerMethodField()

    class Meta:
        model = models.PathfinderMonster
        fields = '__all__'

    def get_initiative(self, monster):
        initiative = (monster.dexterity // 2) - 5
        if 'Improved Initiative' in monster.feats:
            initiative += 4
        return initiative

    def get_perception(self, monster):
        perception = (monster.wisdom // 2) - 5
        if 'Perception' in monster.skills:
            # This might be something like "+37 *+49 vs. traps" but we only care about the bas here
            perception += int(monster.skills['Perception'][1:].split(' ')[0])
        return perception


class FifthEditionMonsterSerializer(serializers.HyperlinkedModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    str_mod = serializers.SerializerMethodField()
    dex_mod = serializers.SerializerMethodField()
    con_mod = serializers.SerializerMethodField()
    int_mod = serializers.SerializerMethodField()
    wis_mod = serializers.SerializerMethodField()
    cha_mod = serializers.SerializerMethodField()

    class Meta:
        model = models.FifthEditionMonster
        fields = '__all__'

    def get_str_mod(self, monster):
        if monster.strength > 10:
            return f'+{int((monster.strength - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.strength) / 2)}'

    def get_dex_mod(self, monster):
        if monster.dexterity > 10:
            return f'+{int((monster.dexterity - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.dexterity) / 2)}'

    def get_con_mod(self, monster):
        if monster.constitution > 10:
            return f'+{int((monster.constitution - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.constitution) / 2)}'

    def get_int_mod(self, monster):
        if monster.intelligence > 10:
            return f'+{int((monster.intelligence - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.intelligence) / 2)}'

    def get_wis_mod(self, monster):
        if monster.wisdom > 10:
            return f'+{int((monster.wisdom - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.wisdom) / 2)}'

    def get_cha_mod(self, monster):
        if monster.charisma > 10:
            return f'+{int((monster.charisma - 10) / 2)}'
        else:
            return f'-{math.ceil((10 - monster.charisma) / 2)}'