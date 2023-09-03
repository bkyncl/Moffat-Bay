# Generated by Django 4.2.4 on 2023-09-02 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoomChoices',
            fields=[
                ('choiceID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('roomSize', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Room Size Choices',
            },
        ),
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('roomID', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomchoices', to_field='roomSize')),
            ],
            options={
                'verbose_name_plural': 'Lodge Rooms',
            },
        ),
    ]
