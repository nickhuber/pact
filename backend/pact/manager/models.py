from django.contrib import auth
from django.core.exceptions import ValidationError
from django.db import models

import dice

import uuid


class UUIDPrimaryKeyModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
    )

    class Meta:
        abstract = True


class ArchiveModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(archived=True)


class ArchiveModel(models.Model):
    archived = models.BooleanField(default=False, db_index=True)
    objects = ArchiveModelManager()
    archived_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.archived = True
        self.save()


class Character(ArchiveModel, UUIDPrimaryKeyModel):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, default='', blank=True)
    hit_dice = models.CharField(max_length=128, default='', blank=True)
    is_player = models.BooleanField(default=False, db_index=True)
    created_by = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)
    speed_stat = models.IntegerField(null=True, default=None, blank=True)

    def __str__(self):
        return self.name

    @property
    def is_npc(self):
        return not self.is_player

    def clean(self):
        if self.is_npc and not self.hit_dice:
            raise ValidationError(
                {'hit_dice': 'Hit dice required for NPCs.'}
            )
        if self.is_player and self.hit_dice:
            raise ValidationError(
                {'hit_dice': 'Hit dice cannot be used for players.'}
            )


class Encounter(ArchiveModel, UUIDPrimaryKeyModel):
    name = models.CharField(max_length=256)
    characters = models.ManyToManyField(
        Character,
        through='EncounterCharacter'
    )
    notes = models.TextField(max_length=8192, blank=True, default='')
    current_initiative = models.IntegerField(null=True, blank=True)
    current_speed_stat = models.IntegerField(null=True, blank=True)
    current_round = models.IntegerField(default=0)
    created_by = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # TODO: move this to the serializer
    @property
    def active_character_uuids(self):
        if self.current_initiative is None:
            return []
        characters_query = self.encountercharacter_set\
            .filter(initiative=self.current_initiative)
        if self._use_speed_stat:
            characters_query = characters_query\
                .filter(character__speed_stat=self.current_speed_stat)
        return [c.uuid for c in characters_query]

    @property
    def _use_speed_stat(self):
        return not self.encountercharacter_set\
            .filter(initiative=self.current_initiative)\
            .filter(character__speed_stat=None)\
            .exists()

    @property
    def _next_speed_stat(self):
        speed_stat_query = self.encountercharacter_set\
            .filter(initiative=self.current_initiative)\
            .order_by('-character__speed_stat')
        if self.current_speed_stat is not None:
            speed_stat_query = speed_stat_query\
                .filter(character__speed_stat__lt=self.current_speed_stat)
        return speed_stat_query.first().character.speed_stat

    @property
    def _next_initiative(self):
        initiative_query = self.encountercharacter_set\
            .exclude(initiative=None)
        if self.current_initiative is not None:
            initiative_query = initiative_query\
                .filter(initiative__lt=self.current_initiative)
        return initiative_query.order_by('-initiative').first().initiative

    def advance_initiative(self):
        if not self.encountercharacter_set.exclude(initiative=None).exists():
            return

        if self.current_initiative is None:
            # Initiative hasn't started yet, so just grab the first character
            self.current_initiative = self._next_initiative
            if self._use_speed_stat:
                self.current_speed_stat = self._next_speed_stat
        else:
            # Find the next Character
            try:
                if self._use_speed_stat:
                    try:
                        self.current_speed_stat = self._next_speed_stat
                    except (AttributeError, EncounterCharacter.DoesNotExist):
                        # No more speed stats at this level, next initiative
                        self.current_speed_stat = None
                        self.current_initiative = self._next_initiative
                        if self._use_speed_stat:
                            self.current_speed_stat = self._next_speed_stat
                else:
                    self.current_speed_stat = None
                    self.current_initiative = self._next_initiative
                    if self._use_speed_stat:
                        self.current_speed_stat = self._next_speed_stat
            except (AttributeError, EncounterCharacter.DoesNotExist):
                # No more initatitives, roll over
                self.current_initiative = None
                self.current_speed_stat = None
                self.current_initiative = self._next_initiative
                if self._use_speed_stat:
                    self.current_speed_stat = self._next_speed_stat
                self.current_round += 1

        self.save()
        self.handle_initiative_changed()

    # TODO: make this a post-save signal that does things if init or speed_stat change
    def handle_initiative_changed(self):
        encounter_characters = self.encountercharacter_set.filter(
            initiative=self.current_initiative,
        )
        if self._use_speed_stat:
            encounter_characters.filter(
                character__speed_stat=self.current_speed_stat,
            )
        for ec in encounter_characters:
            for status in ec.statuseffect_set.all():
                status.reduce()


class EncounterCharacter(ArchiveModel, UUIDPrimaryKeyModel):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    initiative = models.IntegerField(null=True)
    max_hp = models.IntegerField(null=True)
    current_hp = models.IntegerField(null=True)
    notes = models.CharField(max_length=128, default='', blank=True)

    def __str__(self):
        return '{}: {}'.format(self.encounter.name, self.name)

    @property
    def name(self):
        return self.character.name

    def save(self, *args, **kwargs):
        # Probably nicer to do this with a signal or something
        if self.character.is_npc:
            # TODO: abstract this part away
            if self.max_hp is None:
                results = dice.roll(self.character.hit_dice)
                try:
                    # For some reason dice.roll will give us a list of the
                    # dice rolls if asking for a single type, like "3d6"
                    # instead of "3d6 + 1"
                    results = sum(results)
                except TypeError:
                    pass
                self.max_hp = results

            if self.current_hp is None:
                self.current_hp = self.max_hp

        super().save(*args, **kwargs)


class StatusEffect(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=64)
    remaining_duration = models.IntegerField()
    character = models.ForeignKey(EncounterCharacter, on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.character.name, self.name)

    def reduce(self):
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.delete()
        else:
            self.save()
