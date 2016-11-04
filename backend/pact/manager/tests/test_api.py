from django.contrib.auth.models import User
from django.test import TestCase, Client

from rest_framework import status

from manager import models


class APITestCase(TestCase):
    def setUp(self):
        self.main_user = User.objects.create(username='main', is_active=True)
        self.other_user = User.objects.create(username='secondary', is_active=True)
        self.client = Client()

    def login(self):
        self.client.force_login(self.main_user)

    def logout(self):
        self.client.logout()


class CharacterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            created_by=self.main_user,
            name='test',
            is_player=True
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_character_is_archived(self):
        response = self.client.delete('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        character = models.Character.archived_objects.get(uuid=self.character.uuid)
        self.assertTrue(character.archived)

    def test_delete_character_cant_be_fetched(self):
        response = self.client.delete('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_fetch_character_from_other_user(self):
        self.character.created_by = self.other_user
        self.character.save()
        response = self.client.get('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EncounterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.encounter = models.Encounter.objects.create(
            created_by=self.main_user,
            name='test',
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_encounter_is_archived(self):
        response = self.client.delete('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        encounter = models.Encounter.archived_objects.get(uuid=self.encounter.uuid)
        self.assertTrue(encounter.archived)

    def test_delete_encounter_cant_be_fetched(self):
        response = self.client.delete('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_fetch_encounter_from_other_user(self):
        self.encounter.created_by = self.other_user
        self.encounter.save()
        response = self.client.get('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EncounterCharacterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            created_by=self.main_user,
            name='test',
            is_player=True
        )
        self.encounter = models.Encounter.objects.create(
            created_by=self.main_user,
            name='test',
        )
        self.encountercharacter = models.EncounterCharacter.objects.create(
            character=self.character,
            encounter=self.encounter,
            initiative=1
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/encounter_characters/{uuid}'.format(
            uuid=self.encountercharacter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_encountercharacter_is_archived(self):
        response = self.client.delete('/api/encounter_characters/{uuid}'.format(
            uuid=self.encountercharacter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        encountercharacter = models.EncounterCharacter.archived_objects.get(uuid=self.encountercharacter.uuid)
        self.assertTrue(encountercharacter.archived)

    def test_delete_encountercharacter_cant_be_fetched(self):
        response = self.client.delete('/api/encounter_characters/{uuid}'.format(
            uuid=self.encountercharacter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/encounter_characters/{uuid}'.format(
            uuid=self.encountercharacter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_fetch_encountercharacter_from_other_user(self):
        self.encounter.created_by = self.other_user
        self.encounter.save()
        response = self.client.get('/api/encounter_characters/{uuid}'.format(
            uuid=self.encountercharacter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class StatusEffectUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            created_by=self.main_user,
            name='test',
            is_player=True
        )
        self.encounter = models.Encounter.objects.create(
            created_by=self.main_user,
            name='test',
        )
        self.encountercharacter = models.EncounterCharacter.objects.create(
            character=self.character,
            encounter=self.encounter,
            initiative=1
        )
        self.statuseffect = models.StatusEffect.objects.create(
            name='status',
            remaining_duration=2,
            character=self.encountercharacter
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/status_effects/{uuid}'.format(
            uuid=self.statuseffect.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_status_effect_is_deleted(self):
        response = self.client.delete('/api/status_effects/{uuid}'.format(
            uuid=self.statuseffect.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.StatusEffect.objects.filter(uuid=self.statuseffect.uuid).exists())

    def test_delete_status_effect_cant_be_fetched(self):
        response = self.client.delete('/api/status_effects/{uuid}'.format(
            uuid=self.statuseffect.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get('/api/status_effects/{uuid}'.format(
            uuid=self.statuseffect.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cant_fetch_status_effect_from_other_user(self):
        self.encounter.created_by = self.other_user
        self.encounter.save()
        response = self.client.get('/api/status_effects/{uuid}'.format(
            uuid=self.statuseffect.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)