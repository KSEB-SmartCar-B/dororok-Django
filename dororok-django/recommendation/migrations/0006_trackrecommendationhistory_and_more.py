# Generated by Django 4.2.14 on 2024-08-25 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0005_dororokdestination'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackRecommendationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('artist', models.CharField(max_length=255)),
                ('track_id', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'track_recommendation_history',
                'managed': True,
            },
        ),
        migrations.AlterModelTable(
            name='dororokdestination',
            table='destination',
        ),
    ]
