from django.contrib import admin
from manager import models


admin.site.register(models.Character)
admin.site.register(models.Encounter)
admin.site.register(models.EncounterCharacter)
admin.site.register(models.StatusEffect)
