# Generated by Django 5.0.4 on 2024-04-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grabproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='folder_path',
            field=models.CharField(default='newfile', max_length=255),
            preserve_default=False,
        ),
    ]