# Generated by Django 2.2 on 2019-04-21 17:40

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PathfinderMonster',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('cr', models.FloatField(blank=True, null=True)),
                ('xp', models.IntegerField(blank=True, null=True)),
                ('race', models.CharField(blank=True, max_length=64, null=True)),
                ('classes', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('alignment', models.TextField(blank=True, max_length=2, null=True)),
                ('size', models.CharField(blank=True, max_length=64, null=True)),
                ('type', models.CharField(blank=True, max_length=64, null=True)),
                ('subtypes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), default=list, size=None)),
                ('ac', models.IntegerField(blank=True, null=True)),
                ('ac_touch', models.IntegerField(blank=True, null=True)),
                ('ac_flat_footed', models.IntegerField(blank=True, null=True)),
                ('hp', models.IntegerField(blank=True, null=True)),
                ('hit_dice', models.CharField(blank=True, max_length=128, null=True)),
                ('fortitude_save', models.TextField(blank=True, null=True)),
                ('reflex_save', models.TextField(blank=True, null=True)),
                ('will_save', models.TextField(blank=True, null=True)),
                ('melee_attack', models.TextField(blank=True, null=True)),
                ('ranged_attack', models.TextField(blank=True, null=True)),
                ('reach', models.TextField(blank=True, null=True)),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('dexterity', models.IntegerField(blank=True, null=True)),
                ('constitution', models.IntegerField(blank=True, null=True)),
                ('intelligence', models.IntegerField(blank=True, null=True)),
                ('wisdom', models.IntegerField(blank=True, null=True)),
                ('charisma', models.IntegerField(blank=True, null=True)),
                ('feats', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), default=list, size=None)),
                ('skills', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('racial_mods', models.TextField(blank=True, null=True)),
                ('languages', models.TextField(blank=True, null=True)),
                ('special_qualities', models.TextField(blank=True, null=True)),
                ('environment', models.TextField(blank=True, null=True)),
                ('organization', models.TextField(blank=True, null=True)),
                ('treasure', models.TextField(blank=True, null=True)),
                ('group', models.TextField(blank=True, null=True)),
                ('gear', models.TextField(blank=True, null=True)),
                ('other_gear', models.TextField(blank=True, null=True)),
                ('is_character', models.BooleanField(blank=True, null=True)),
                ('is_companion', models.BooleanField(blank=True, null=True)),
                ('speed', models.TextField(blank=True, null=True)),
                ('base_speed', models.TextField(blank=True, null=True)),
                ('fly_speed', models.TextField(blank=True, null=True)),
                ('maneuverability', models.TextField(blank=True, null=True)),
                ('climb_speed', models.TextField(blank=True, null=True)),
                ('swim_speed', models.TextField(blank=True, null=True)),
                ('burrow_speed', models.TextField(blank=True, null=True)),
                ('speed_special', models.TextField(blank=True, help_text='Any other special movement rules not covered by the basics', null=True)),
                ('can_walk', models.BooleanField(blank=True, null=True)),
                ('can_fly', models.BooleanField(blank=True, null=True)),
                ('can_climb', models.BooleanField(blank=True, null=True)),
                ('can_burrow', models.BooleanField(blank=True, null=True)),
                ('can_swim', models.BooleanField(blank=True, null=True)),
                ('variant_parent', models.TextField(blank=True, help_text='What kind of creature is this based on', null=True)),
                ('class_archetypes', models.TextField(blank=True, null=True)),
                ('companion_familiar_link', models.TextField(blank=True, null=True)),
                ('alternate_name_form', models.TextField(blank=True, help_text='For a shapershifter, what is the name of the other form', null=True)),
                ('original_id', models.IntegerField(blank=True, null=True)),
                ('is_unique_monster', models.BooleanField(blank=True, null=True)),
                ('mythic_rank', models.IntegerField(blank=True, null=True)),
                ('is_mythic', models.BooleanField(blank=True, null=True)),
                ('mythic_tier', models.IntegerField(blank=True, null=True)),
                ('source_book', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]