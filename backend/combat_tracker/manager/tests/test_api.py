from django.contrib.auth.models import User
from django.test import TestCase, Client

from rest_framework import status

from manager import models


class APITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test', is_active=True)
        self.client = Client()

    def login(self):
        self.client.force_login(self.user)

    def logout(self):
        self.client.logout()


class CharacterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            name='test',
            is_player=True
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/characters/{uuid}'.format(
            uuid=self.character.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EncounterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.encounter = models.Encounter.objects.create(
            name='test',
        )
        self.login()

    def test_get_by_uuid(self):
        response = self.client.get('/api/encounters/{uuid}'.format(
            uuid=self.encounter.uuid
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EncounterCharacterUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            name='test',
            is_player=True
        )
        self.encounter = models.Encounter.objects.create(
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


class StatusEffectUUIDLookupTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.character = models.Character.objects.create(
            name='test',
            is_player=True
        )
        self.encounter = models.Encounter.objects.create(
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
