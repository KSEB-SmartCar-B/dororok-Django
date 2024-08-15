# Generated by Django 4.2.14 on 2024-08-14 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0004_alter_dororokfavoritegenre_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='DororokDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_range', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=255)),
                ('region1depth_name', models.CharField(max_length=255)),
                ('region2depth_name', models.CharField(max_length=255)),
                ('region3depth_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'destinations',
                'managed': False,
            },
        ),
    ]
