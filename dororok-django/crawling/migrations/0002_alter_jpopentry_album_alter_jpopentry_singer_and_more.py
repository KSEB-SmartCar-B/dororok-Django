# Generated by Django 4.2.14 on 2024-08-06 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jpopentry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='jpopentry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ostentry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ostentry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='popentry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='popentry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 rbsoulentry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 rbsoulentry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 랩힙합entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 랩힙합entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 록메탈entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 록메탈entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 밴드entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 밴드entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 포크블루스entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='국내 포크블루스entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='뉴에이지entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='뉴에이지entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='댄스entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='댄스entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='발라드entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='발라드entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='인디entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='인디entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='일렉트로니카entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='일렉트로니카entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='재즈entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='재즈entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='클래식entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='클래식entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='트로트entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='트로트entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 rbsoulentry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 rbsoulentry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 랩힙합entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 랩힙합entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 록메탈entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 록메탈entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 밴드entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 밴드entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 포크블루스컨트리entry',
            name='album',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='해외 포크블루스컨트리entry',
            name='singer',
            field=models.CharField(max_length=255),
        ),
    ]
