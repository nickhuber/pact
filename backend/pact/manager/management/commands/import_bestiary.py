import csv

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from manager.models import PathfinderMonster


subtype_fields = ['subtype1', 'subtype2', 'subtype3', 'subtype4', 'subtype5', 'subtype6']


class Command(BaseCommand):
    help = 'Import Pathfinder bestiary data into the local database'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        PathfinderMonster.objects.all().delete()
        with open(options['file'], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if PathfinderMonster.objects.filter(name=row['Name']).exists():
                        self.stdout.write(self.style.ERROR(f"Skipping {row['Name']} as it already exists"))
                        continue
                    subtypes = []
                    for s in subtype_fields:
                        if row[s]:
                            subtypes.append(row[s])
                    classes = []
                    if row['Class1'] != '':
                        classes.append({'class': row['Class1'], 'level': row['Class1_Lvl']})
                    if row['Class2'] != '':
                        classes.append({'class': row['Class2'], 'level': row['Class2_Lvl']})
                    skills = {}
                    for skill in row['Skills'].split(','):
                        skill = skill.strip()
                        if '+' in skill:
                            s, mod = skill.split('+', 1)
                            skills[s.strip()] = f'+{mod.strip()}'
                        elif '-' in skill:
                            s, mod = skill.split('-', 1)
                            skills[s.strip()] = f'-{mod.strip()}'
                        else:
                            continue
                    feats = []
                    for feat in row['Feats'].split(', '):
                        feats.append(feat)
                    monster = PathfinderMonster.objects.create(
                        name=row['Name'],
                        cr=row['CR'] if row['CR'] != '' else None,
                        xp=int(row['XP'].replace(',', '')) if row['XP'] != '' else None,
                        race=row['Race'] if row['Race'] != '' else None,
                        classes=classes,
                        alignment=row['Alignment'] if row['Alignment'] != '' else None,
                        size=row['Size'] if row['Size'] != '' else None,
                        type=row['Type'] if row['Type'] != '' else None,
                        subtypes=subtypes,
                        ac=row['AC'] if row['AC'] != '' else None,
                        ac_touch=row['AC_Touch'] if row['AC_Touch'] != '' else None,
                        ac_flat_footed=row['AC_Flat-footed'] if row['AC_Flat-footed'] != '' else None,
                        hp=row['HP'] if row['HP'] != '' else None,
                        hit_dice=row['HD'] if row['HD'] != '' else None,
                        fortitude_save=row['Fort'] if row['Fort'] != '' else None,
                        reflex_save=row['Ref'] if row['Ref'] != '' else None,
                        will_save=row['Will'] if row['Will'] != '' else None,
                        melee_attack=row['Melee'] if row['Melee'] != '' else None,
                        ranged_attack=row['Ranged'] if row['Ranged'] != '' else None,
                        reach=row['Reach'] if row['Reach'] != '' else None,
                        strength=row['Str'] if row['Str'] != '-' else None,
                        dexterity=row['Dex'] if row['Dex'] != '-' else None,
                        constitution=row['Con'] if row['Con'] != '-' else None,
                        intelligence=row['Int'] if row['Int'] != '-' else None,
                        wisdom=row['Wis'] if row['Wis'] != '-' else None,
                        charisma=row['Cha'] if row['Cha'] != '-' else None,
                        feats=feats,
                        skills=skills,
                        racial_mods=row['RacialMods'] if row['RacialMods'] != '' else None,
                        languages=row['Languages'] if row['Languages'] != '' else None,
                        special_qualities=row['SQ'] if row['SQ'] != '' else None,
                        environment=row['Environment'] if row['Environment'] != '' else None,
                        organization=row['Organization'] if row['Organization'] != '' else None,
                        treasure=row['Treasure'] if row['Treasure'] != '' else None,
                        group=row['Group'] if row['Group'] != '' else None,
                        gear=row['Gear'] if row['Gear'] != '' else None,
                        other_gear=row['OtherGear'] if row['OtherGear'] != '' else None,
                        is_character=row['CharacterFlag'] if row['CharacterFlag'] != '' else None,
                        is_companion=row['CompanionFlag'] if row['CompanionFlag'] != '' else None,
                        speed=row['Speed'] if row['Speed'] != '' else None,
                        base_speed=row['Base_Speed'] if row['Base_Speed'] != '' else None,
                        fly_speed=row['Fly_Speed'] if row['Fly_Speed'] != '' else None,
                        maneuverability=row['Maneuverability'] if row['Maneuverability'] != '' else None,
                        climb_speed=row['Climb_Speed'] if row['Climb_Speed'] != '' else None,
                        swim_speed=row['Swim_Speed'] if row['Swim_Speed'] != '' else None,
                        burrow_speed=row['Burrow_Speed'] if row['Burrow_Speed'] != '' else None,
                        speed_special=row['Speed_Special'] if row['Speed_Special'] != '' else None,
                        can_walk=row['Speed_Land'] if row['Speed_Land'] != '' else None,
                        can_fly=row['Fly'] if row['Fly'] != '' else None,
                        can_climb=row['Climb'] if row['Climb'] != '' else None,
                        can_burrow=row['Burrow'] if row['Burrow'] != '' else None,
                        can_swim=row['Swim'] if row['Swim'] != '' else None,
                        variant_parent=row['VariantParent'] if row['VariantParent'] not in ['NULL', ''] else None,
                        class_archetypes=row['ClassArchetypes'] if row['ClassArchetypes'] != '' else None,
                        companion_familiar_link=row['CompanionFamiliarLink'] if row['CompanionFamiliarLink'] not in ['NULL', ''] else None,
                        alternate_name_form=row['AlternateNameForm'] if row['AlternateNameForm'] != '' else None,
                        original_id=row['id'] if row['id'] != '' else None,
                        is_unique_monster=row['UniqueMonster'] if row['UniqueMonster'] != '' else None,
                        mythic_rank=row['MR'] if row['MR'] != '' else None,
                        is_mythic=row['Mythic'] if row['Mythic'] != '' else None,
                        mythic_tier=row['MT'] if row['MT'] != '' else None,
                        source_book=row['Source'] if row['Source'] != '' else None,
                    )
                    self.stdout.write(self.style.SUCCESS(f'Imported {monster.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Exception importing data: {e}'))
                    self.stdout.write(self.style.ERROR(str(row)))
                    raise
