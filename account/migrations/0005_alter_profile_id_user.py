# Generated by Django 4.2.3 on 2024-03-18 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_profile_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id_user',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]