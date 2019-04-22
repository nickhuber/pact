from django.contrib import auth
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

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
    current_round = models.IntegerField(default=0)
    created_by = models.ForeignKey(auth.models.User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_next_initiative(self):
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
            self.current_initiative = self.get_next_initiative()
        else:
            # Find the next Character
            try:
                self.current_initiative = self.get_next_initiative()
            except (AttributeError, EncounterCharacter.DoesNotExist):
                # No more initatitives, roll over
                self.current_initiative = None
                self.current_initiative = self.get_next_initiative()
                self.current_round += 1

        self.save()
        self.handle_initiative_changed()

    # TODO: make this a post-save signal that does things if init changes
    def handle_initiative_changed(self):
        encounter_characters = self.encountercharacter_set.filter(
            initiative=self.current_initiative,
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


class PathfinderMonster(UUIDPrimaryKeyModel):
    name = models.CharField(max_length=256, unique=True)
    cr = models.FloatField(null=True, blank=True)
    xp = models.IntegerField(null=True, blank=True)
    race = models.CharField(max_length=64, null=True, blank=True)
    classes = JSONField(default=list)
    alignment = models.TextField(max_length=2, null=True, blank=True)
    size = models.CharField(max_length=64, null=True, blank=True)
    type = models.CharField(max_length=64, null=True, blank=True)
    subtypes = ArrayField(models.CharField(max_length=128), default=list)
    ac = models.IntegerField(null=True, blank=True)
    ac_touch = models.IntegerField(null=True, blank=True)
    ac_flat_footed = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    hit_dice = models.CharField(max_length=128, null=True, blank=True)
    fortitude_save = models.TextField(null=True, blank=True)
    reflex_save = models.TextField(null=True, blank=True)
    will_save = models.TextField(null=True, blank=True)
    melee_attack = models.TextField(null=True, blank=True)
    ranged_attack = models.TextField(null=True, blank=True)
    reach = models.TextField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    dexterity = models.IntegerField(null=True, blank=True)
    constitution = models.IntegerField(null=True, blank=True)
    intelligence = models.IntegerField(null=True, blank=True)
    wisdom = models.IntegerField(null=True, blank=True)
    charisma = models.IntegerField(null=True, blank=True)
    feats = ArrayField(models.CharField(max_length=128), default=list)
    skills = JSONField(null=True, blank=True)
    racial_mods = models.TextField(null=True, blank=True)
    languages = models.TextField(null=True, blank=True)
    special_qualities = models.TextField(null=True, blank=True)
    environment = models.TextField(null=True, blank=True)
    organization = models.TextField(null=True, blank=True)
    treasure = models.TextField(null=True, blank=True)
    group = models.TextField(null=True, blank=True)
    gear = models.TextField(null=True, blank=True)
    other_gear = models.TextField(null=True, blank=True)
    is_character = models.BooleanField(null=True, blank=True)
    is_companion = models.BooleanField(null=True, blank=True)
    speed = models.TextField(null=True, blank=True)
    base_speed = models.TextField(null=True, blank=True)
    fly_speed = models.TextField(null=True, blank=True)
    maneuverability = models.TextField(null=True, blank=True)
    climb_speed = models.TextField(null=True, blank=True)
    swim_speed = models.TextField(null=True, blank=True)
    burrow_speed = models.TextField(null=True, blank=True)
    speed_special = models.TextField(null=True, blank=True, help_text="Any other special movement rules not covered by the basics")
    can_walk = models.BooleanField(null=True, blank=True)
    can_fly = models.BooleanField(null=True, blank=True)
    can_climb = models.BooleanField(null=True, blank=True)
    can_burrow = models.BooleanField(null=True, blank=True)
    can_swim = models.BooleanField(null=True, blank=True)
    variant_parent = models.TextField(null=True, blank=True, help_text="What kind of creature is this based on")
    class_archetypes = models.TextField(null=True, blank=True)
    companion_familiar_link = models.TextField(null=True, blank=True)
    alternate_name_form = models.TextField(null=True, blank=True, help_text="For a shapershifter, what is the name of the other form")
    original_id = models.IntegerField(null=True, blank=True)
    is_unique_monster = models.BooleanField(null=True, blank=True)
    mythic_rank = models.IntegerField(null=True, blank=True)
    is_mythic = models.BooleanField(null=True, blank=True)
    mythic_tier = models.IntegerField(null=True, blank=True)
    source_book = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
