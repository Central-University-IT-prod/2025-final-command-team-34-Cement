# Generated by Django 5.1.6 on 2025-03-02 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_mentorprofile_rating_count_mentorprofile_rating_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.URLField(default='no'),
            preserve_default=False,
        ),
    ]
