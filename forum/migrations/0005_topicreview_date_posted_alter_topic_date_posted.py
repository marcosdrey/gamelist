# Generated by Django 5.0.4 on 2024-08-26 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_topic_date_edited_topic_is_edited_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='topicreview',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, default=None, verbose_name='Data Postada'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data Postada'),
        ),
    ]