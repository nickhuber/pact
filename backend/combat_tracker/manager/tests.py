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


class EncounterTestCase(TestCase):
    def setUp(self):
        self.encounter = models.Encounter(name='test_encounter')
        self.encounter.save()
        character1 = models.Character(name='test1', is_player=True)
        character1.save()
        character2 = models.Character(name='test2', is_player=True)
        character2.save()
        self.ec1 = models.EncounterCharacter(character=character1, encounter=self.encounter)
        self.ec2 = models.EncounterCharacter(character=character2, encounter=self.encounter)

    def test_advance_init_starts_lowest_init(self):
        self.ec1.initiative = 1
        self.ec1.save()
        self.ec2.initiative = 2
        self.ec2.save()

        self.assertIsNone(self.encounter.current_initiative)
        self.encounter.advance_init()
        self.assertEqual(self.encounter.current_initiative, self.ec1.initiative)

    def test_advance_init_rolls_over_at_highest_init(self):
        self.ec1.initiative = 1
        self.ec1.save()
        self.ec2.initiative = 2
        self.ec2.save()

        self.encounter.current_initiative = 2
        self.encounter.save()

        self.encounter.advance_init()
        self.assertEqual(self.encounter.current_initiative, self.ec1.initiative)
