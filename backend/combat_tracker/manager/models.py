from django.db import models
from django.core.validators import MinValueValidator


class ArchiveModelManager(models.Manager):
    def get_queryset(self):
        return super(ArchiveModelManager, self).get_queryset().exclude(archived=True)


class ArchiveModel(models.Model):
    archived = models.BooleanField(default=False, db_index=True)
    objects = ArchiveModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.archived = True
        self.save()


class Character(ArchiveModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=8192, default='')
    max_hp = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    is_player = models.BooleanField(default=False, db_index=True)


class Encounter(ArchiveModel):
    characters = models.ManyToManyField(Character, through='EncounterCharacter')
    current_initiative = models.IntegerField(null=True)
    current_round = models.IntegerField(default=0)

    def advance_init(self):
        if self.current_initiative is None:
            self.current_initiative = self.characters.order_by('-initiative').first().initiative
            self.current_round += 1
        else:
            try:
                self.current_initiative = self.characters\
                    .filter(initiative__gt=self.current_initiative)\
                    .order_by('-initiative')\
                    .first()\
                    .initiative
            except EncounterCharacter.DoesNotExist:
                self.current_initiative = self.characters.order_by('-initiative').first().initiative
                self.current_round += 1
        self.save()   


class EncounterCharacter(ArchiveModel):
    character = models.ForeignKey(Character)
    encounter = models.ForeignKey(Encounter)
    initiative = models.IntegerField(null=True)
    current_hp = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        if self.current_hp is None:
            self.current_hp = self.character.max_hp

        super(EncounterCharacter, self).save(*args, **kwargs)
