# Generated by Django 4.2.6 on 2023-12-22 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_alter_choice_choice_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='uservote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting', models.IntegerField(default=0)),
            ],
        ),
    ]