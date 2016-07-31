from django.core.exceptions import ValidationError
from django.db import models

import dice


class ArchiveModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(archived=True)


class ArchiveModel(models.Model):
    archived = models.BooleanField(default=False, db_index=True)
    objects = ArchiveModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.archived = True
        self.save()


class Character(ArchiveModel):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=8192, default='', blank=True)
    hit_dice = models.CharField(max_length=128, default='', blank=True)
    is_player = models.BooleanField(default=False, db_index=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.is_player and not self.hit_dice:
            raise ValidationError(
                {'hit_dice': 'Hit dice required for NPCs.'}
            )


class Encounter(ArchiveModel):
    name = models.CharField(max_length=256)
    characters = models.ManyToManyField(
        Character,
        through='EncounterCharacter'
    )
    current_initiative = models.IntegerField(null=True, blank=True)
    current_round = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def advance_initiative(self):
        if not self.encountercharacter_set.all().exists():
            return

        if self.current_initiative is None:
            self.current_initiative = self.encountercharacter_set\
                .exclude(initiative=None)\
                .order_by('-initiative').first().initiative
            self.current_round += 1
        else:
            try:
                # Find the next character
                self.current_initiative = self.encountercharacter_set\
                    .filter(initiative__lt=self.current_initiative)\
                    .exclude(initiative=None)\
                    .order_by('-initiative')\
                    .first()\
                    .initiative
            except (AttributeError, EncounterCharacter.DoesNotExist):
                # Rolled over, back to the first
                self.current_initiative = self.encountercharacter_set\
                    .exclude(initiative=None)\
                    .order_by('-initiative').first().initiative
                self.current_round += 1
        encounter_characters = self.encountercharacter_set.filter(
            initiative=self.current_initiative
        )
        for ec in encounter_characters:
            for status in ec.statuseffect_set.all():
                status.reduce()
        self.save()


class EncounterCharacter(ArchiveModel):
    character = models.ForeignKey(Character)
    encounter = models.ForeignKey(Encounter)
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
        if not self.character.is_player:
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


class StatusEffect(models.Model):
    name = models.CharField(max_length=64)
    remaining_duration = models.IntegerField()
    character = models.ForeignKey(EncounterCharacter)

    def __str__(self):
        return '{}: {}'.format(self.character.name, self.name)

    def reduce(self):
        self.remaining_duration -= 1
        if self.remaining_duration <= 0:
            self.delete()
        else:
            self.save()
