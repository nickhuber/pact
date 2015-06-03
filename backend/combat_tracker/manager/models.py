from django.db import models


class PlayerCharacter(models.Model):
    name = models.CharField(max_length=128)


class NPCTemplate(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=8192)
    max_hp = models.IntegerField()


class Encounter(models.Model):
    name = models.CharField(max_length=512)
    npcs = models.ManyToManyField(NPCTemplate, through='EncounterNPC')
    players = models.ManyToManyField(PlayerCharacter)


class EncounterNPC(models.Model):
    npc_template = models.ForeignKey(NPCTemplate)
    encounter = models.ForeignKey(Encounter)
    current_hp = models.IntegerField()

