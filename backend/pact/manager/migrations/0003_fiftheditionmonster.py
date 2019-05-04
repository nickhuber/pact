# Generated by Django 2.2 on 2019-05-04 04:08

import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_pathfindermonster'),
    ]

    operations = [
        migrations.CreateModel(
            name='FifthEditionMonster',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('description', models.TextField()),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), default=list, size=None)),
                ('cr', models.CharField(blank=True, max_length=256, null=True)),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('dexterity', models.IntegerField(blank=True, null=True)),
                ('constitution', models.IntegerField(blank=True, null=True)),
                ('intelligence', models.IntegerField(blank=True, null=True)),
                ('wisdom', models.IntegerField(blank=True, null=True)),
                ('charisma', models.IntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=256, null=True)),
                ('alignment', models.CharField(blank=True, max_length=256, null=True)),
                ('challenge', models.CharField(blank=True, max_length=256, null=True)),
                ('languages', models.CharField(blank=True, max_length=256, null=True)),
                ('senses', models.CharField(blank=True, max_length=256, null=True)),
                ('skills', models.CharField(blank=True, max_length=256, null=True)),
                ('damage_immunities', models.CharField(blank=True, max_length=256, null=True)),
                ('saving_throws', models.CharField(blank=True, max_length=256, null=True)),
                ('speed', models.CharField(blank=True, max_length=256, null=True)),
                ('hit_points_avg', models.IntegerField(blank=True, null=True)),
                ('hit_dice', models.CharField(blank=True, max_length=256, null=True)),
                ('armor_class', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
