from django.contrib import admin
from manager.models import Character, Encounter, EncounterCharacter, StatusEffect


admin.site.register(Character)
admin.site.register(Encounter)
admin.site.register(EncounterCharacter)
admin.site.register(StatusEffect)
