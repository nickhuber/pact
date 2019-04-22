from django.contrib import admin
from manager import models

admin.site.register(models.EncounterCharacter)
admin.site.register(models.StatusEffect)

@admin.register(models.Encounter)
class PathfinderMonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_round', 'created_by')


@admin.register(models.Character)
class PathfinderMonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'hit_dice', 'is_player', 'created_by')


@admin.register(models.PathfinderMonster)
class PathfinderMonsterAdmin(admin.ModelAdmin):
    list_display = ('name', 'cr', 'alignment', 'type', 'size')
