# Generated by Django 5.0.4 on 2024-04-27 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grabproject', '0006_delete_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projectname', models.CharField(max_length=30)),
                ('projectzipfile', models.FileField(upload_to='media/')),
            ],
        ),
    ]
