from django.core.exceptions import ValidationError
from django.test import TestCase

from manager import models


class CharacterTestCase(TestCase):
    def test_create_npc_no_hitdice_fails(self):
        character = models.Character(
            name='test',
            is_player=False,
            hit_dice=''
        )
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_create_npc_with_hitdice_succeeds(self):
        character = models.Character(
            name='test',
            is_player=False,
            hit_dice='1d6'
        )
        character.full_clean()

    def test_create_player_with_hitdice_fails(self):
        character = models.Character(
            name='test',
            is_player=True,
            hit_dice='1d6'
        )
        with self.assertRaises(ValidationError):
            character.full_clean()

    def test_create_player_no_hitdice_succeeds(self):
        character = models.Character(
            name='test',
            is_player=True,
            hit_dice=''
        )
        character.full_clean()


class CreateEncounterCharacterTestCase(TestCase):
    def setUp(self):
        self.character = models.Character(name='test_character')
        self.character.save()
        self.encounter = models.Encounter(name='test_encounter')
        self.encounter.save()

    def test_with_hit_dice_makes_max_hp(self):
        self.character.hit_dice = '3d6'
        self.character.save()
        ec = models.EncounterCharacter(
            character=self.character,
            encounter=self.encounter
        )
        ec.save()
        self.assertIsNotNone(ec.max_hp)

    def test_with_hit_dice_makes_current_hp_equal_max_hp(self):
        self.character.hit_dice = '3d6'
        self.character.save()
        ec = models.EncounterCharacter(
            character=self.character,
            encounter=self.encounter
        )
        ec.save()
        self.assertIsNotNone(ec.current_hp)
        self.assertEqual(ec.max_hp, ec.current_hp)


def StatusEffectTestCase(TestCase):
    def setUp(self):
        self.encounter = models.Encounter.objects.create(
            name='test_encounter'
        )
        self.character = models.Character.objects.create(
            name='test',
            is_player=True
        )
        self.ec = models.EncounterCharacter.objects.create(
            character=self.character,
            encounter=self.encounter,
            initiative=1
        )
        self.status = models.StatusEffect.objects.create(
            name='status',
            remaining_duration=2,
            character=self.sc2
        )

    def test_reduce_lowers_duration(self):
        self.status.reduce()
        self.assertEqual(self.remaining_duration, 1)

    def test_reduce_deletes_at_1(self):
        self.status.remaining_duration = 1
        self.status.reduce()
        self.assertFalse(
            models.StatusEffect.objects.filter(id=self.status.id).exists()
        )


class AdvanceInitiativeTestCase(TestCase):
    def setUp(self):
        self.encounter = models.Encounter.objects.create(
            name='test_encounter'
        )
        pending_character = models.Character.objects.create(
            name='test0',
            is_player=True
        )
        character1 = models.Character.objects.create(
            name='test1',
            is_player=True
        )
        character2 = models.Character.objects.create(
            name='test2',
            is_player=True
        )
        character3 = models.Character.objects.create(
            name='test3',
            is_player=True
        )
        self.ecpending = models.EncounterCharacter.objects.create(
            character=pending_character,
            encounter=self.encounter
        )
        self.ec1 = models.EncounterCharacter.objects.create(
            character=character1,
            encounter=self.encounter,
            initiative=1
        )
        self.ec2 = models.EncounterCharacter.objects.create(
            character=character2,
            encounter=self.encounter,
            initiative=2
        )
        self.ec3 = models.EncounterCharacter.objects.create(
            character=character3,
            encounter=self.encounter,
            initiative=3
        )

    def test_starts_highest_init(self):
        self.assertIsNone(self.encounter.current_initiative)
        self.encounter.advance_initiative()
        self.assertEqual(
            self.encounter.current_initiative,
            self.ec3.initiative
        )

    def test_increases_normally(self):
        self.encounter.current_initiative = self.ec3.initiative
        self.encounter.advance_initiative()
        self.assertEqual(
            self.encounter.current_initiative,
            self.ec2.initiative
        )

    def test_rolls_over_at_lowest_init(self):
        self.encounter.current_initiative = self.ec1.initiative

        self.encounter.advance_initiative()
        self.assertEqual(
            self.encounter.current_initiative,
            self.ec3.initiative
        )

    def test_status_effect_duration_decreases_at_start_characters_turn(self):
        self.encounter.current_initiative = self.ec3.initiative
        status = models.StatusEffect.objects.create(
            name='status',
            remaining_duration=2,
            character=self.ec2
        )
        self.encounter.advance_initiative()  # ec2's turn
        status.refresh_from_db()
        self.assertEqual(
            status.remaining_duration,
            1
        )

    def test_status_effect_removes_when_duration_0(self):
        self.encounter.advance_initiative()  # ec3's turn
        status = models.StatusEffect.objects.create(
            name='status',
            remaining_duration=1,
            character=self.ec2
        )
        self.encounter.advance_initiative()  # ec2's turn
        self.assertFalse(
            models.StatusEffect.objects.filter(id=status.id).exists()
        )
