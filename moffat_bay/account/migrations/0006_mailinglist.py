# Generated by Django 4.2.4 on 2023-08-31 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_account_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
            ],
        ),
    ]
