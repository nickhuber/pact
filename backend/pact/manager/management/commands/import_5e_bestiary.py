import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from manager.models import FifthEditionMonster


skipped = (
    # Has a weird hit point range that I don't support
    'shadow-mastiff-alpha.md',
)

class Command(BaseCommand):
    help = 'Import fifth edition bestiary data into the local database'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **options):
        FifthEditionMonster.objects.all().delete()
        for filename in os.listdir(options['directory']):
            if filename in skipped:
                continue
            with open(os.path.join(options['directory'], filename), 'r') as f:
                content = f.read()
                _, stats, description = content.split('---\n')
                monster = FifthEditionMonster()
                for line in stats.split('\n'):
                    if line.startswith('name:'):
                        monster.name = line[7:-1]
                    if line.startswith('tags:'):
                        tags = line[7:-1]
                        for tag in tags.split(', '):
                            if tag.startswith('cr'):
                                monster.cr = tag[2:]
                            else:
                                monster.tags.append(tag)
                    if line.startswith('cha:'):
                        monster.charisma = int(line[5:].split(' ')[0])
                    if line.startswith('wis:'):
                        monster.wisdom = int(line[5:].split(' ')[0])
                    if line.startswith('int:'):
                        monster.intelligence = int(line[5:].split(' ')[0])
                    if line.startswith('con:'):
                        monster.constitution = int(line[5:].split(' ')[0])
                    if line.startswith('dex:'):
                        monster.dexterity = int(line[5:].split(' ')[0])
                    if line.startswith('str:'):
                        monster.strength = int(line[5:].split(' ')[0])
                    if line.startswith('size:'):
                        monster.size = line[6:]
                    if line.startswith('alignment:'):
                        monster.alignment = line[11:]
                    if line.startswith('challenge:'):
                        monster.challenge = line[12:-1]
                    if line.startswith('languages:'):
                        monster.languages = line[12:-1]
                    if line.startswith('senses:'):
                        monster.senses = line[9:-1]
                    if line.startswith('skills:'):
                        monster.skills = line[9:-1]
                    if line.startswith('saving_throws:'):
                        monster.saving_throws = line[16:-1]
                    if line.startswith('speed:'):
                        monster.speed = line[8:-1]
                    if line.startswith('armor_class:'):
                        monster.armor_class = line[14:-1]
                    if line.startswith('hit_points:'):
                        tmp = line[13:-1]
                        # Special case for avatar of death
                        if tmp == '0':
                            monster.hit_points_avg = monster.hit_dice = '0'
                        else:
                            tmp = tmp.replace(' + ', '+')
                            tmp = tmp.replace(' +', '+')
                            tmp = tmp.replace(' - ', '-')
                            tmp = tmp.replace(' -', '-')
                            monster.hit_points_avg, hit_dice = tmp.split()
                            monster.hit_dice = hit_dice[1:-1]
                monster.description = description
                if FifthEditionMonster.objects.filter(name=monster.name).exists():
                    self.stdout.write(self.style.ERROR(f'Skipping {monster.name} since it already exists.'))
                    continue
                monster.save()
                self.stdout.write(self.style.SUCCESS(f'Imported {monster.name}'))
