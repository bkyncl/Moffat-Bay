# Generated by Django 4.2.4 on 2023-08-30 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stay_Costs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guests', models.IntegerField(unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
