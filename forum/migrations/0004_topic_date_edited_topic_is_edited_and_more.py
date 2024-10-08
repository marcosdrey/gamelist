# Generated by Django 5.0.4 on 2024-08-26 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_remove_topicreview_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='date_edited',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data Editada'),
        ),
        migrations.AddField(
            model_name='topic',
            name='is_edited',
            field=models.BooleanField(default=False, verbose_name='Editado'),
        ),
        migrations.AddField(
            model_name='topicreview',
            name='date_edited',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data Editada'),
        ),
        migrations.AddField(
            model_name='topicreview',
            name='is_edited',
            field=models.BooleanField(default=False, verbose_name='Editado'),
        ),
    ]
