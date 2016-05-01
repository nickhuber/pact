from django.test import TestCase

from manager import models

class EncounterCharacterTestCase(TestCase):
    def setUp(self):
        self.character = models.Character(name='test_character')
        self.character.save()
        self.encounter = models.Encounter(name='test_encounter')
        self.encounter.save()

    def test_create_encounter_character_with_hit_dice_makes_max_hp(self):
        self.character.hit_dice='3d6'
        self.character.save()
        ec = models.EncounterCharacter(character=self.character, encounter=self.encounter)
        ec.save()
        self.assertIsNotNone(ec.max_hp)

    def test_create_encounter_character_with_hit_dice_makes_current_hp_equal_max_hp(self):
        self.character.hit_dice='3d6'
        self.character.save()
        ec = models.EncounterCharacter(character=self.character, encounter=self.encounter)
        ec.save()
        self.assertIsNotNone(ec.max_hp)
        self.assertEqual(ec.max_hp, ec.current_hp)


class EncounterInitiativeTestCase(TestCase):
    def setUp(self):
        self.encounter = models.Encounter(name='test_encounter')
        self.encounter.save()
        pending_character = models.Character.objects.create(name='test0', is_player=True)
        character1 = models.Character.objects.create(name='test1', is_player=True)
        character2 = models.Character.objects.create(name='test2', is_player=True)
        character3 = models.Character.objects.create(name='test3', is_player=True)
        self.ecpending = models.EncounterCharacter.objects.create(character=pending_character, encounter=self.encounter)
        self.ec1 = models.EncounterCharacter.objects.create(character=character1, encounter=self.encounter, initiative=1)
        self.ec2 = models.EncounterCharacter.objects.create(character=character2, encounter=self.encounter, initiative=2)
        self.ec3 = models.EncounterCharacter.objects.create(character=character3, encounter=self.encounter, initiative=3)

    def test_advance_init_starts_highest_init(self):
        self.assertIsNone(self.encounter.current_initiative)
        self.encounter.advance_initiative()
        self.assertEqual(self.encounter.current_initiative, self.ec3.initiative)

    def test_advance_init_increases_normally(self):
        self.encounter.current_initiative = self.ec3.initiative
        self.encounter.advance_initiative()
        self.assertEqual(self.encounter.current_initiative, self.ec2.initiative)

    def test_advance_init_rolls_over_at_lowest_init(self):
        self.encounter.current_initiative = self.ec1.initiative

        self.encounter.advance_initiative()
        self.assertEqual(self.encounter.current_initiative, self.ec3.initiative)
