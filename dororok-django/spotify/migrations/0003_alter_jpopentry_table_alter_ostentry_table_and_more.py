# Generated by Django 4.2.14 on 2024-07-30 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_alter_jpopentry_id_alter_ostentry_id_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='jpopentry',
            table='JPOP_entry',
        ),
        migrations.AlterModelTable(
            name='ostentry',
            table='OST_entry',
        ),
        migrations.AlterModelTable(
            name='popentry',
            table='POP_entry',
        ),
        migrations.AlterModelTable(
            name='국내 rbsoulentry',
            table='국내 RBSOUL_entry',
        ),
        migrations.AlterModelTable(
            name='국내 랩힙합entry',
            table='국내 랩힙합_entry',
        ),
        migrations.AlterModelTable(
            name='국내 록메탈entry',
            table='국내 록메탈_entry',
        ),
        migrations.AlterModelTable(
            name='국내 밴드entry',
            table='국내 밴드_entry',
        ),
        migrations.AlterModelTable(
            name='국내 포크블루스entry',
            table='국내 포크블루스_entry',
        ),
        migrations.AlterModelTable(
            name='뉴에이지entry',
            table='뉴에이지_entry',
        ),
        migrations.AlterModelTable(
            name='댄스entry',
            table='댄스_entry',
        ),
        migrations.AlterModelTable(
            name='발라드entry',
            table='발라드_entry',
        ),
        migrations.AlterModelTable(
            name='인디entry',
            table='인디_entry',
        ),
        migrations.AlterModelTable(
            name='일렉트로니카entry',
            table='일렉트로니카_entry',
        ),
        migrations.AlterModelTable(
            name='재즈entry',
            table='재즈_entry',
        ),
        migrations.AlterModelTable(
            name='클래식entry',
            table='클래식_entry',
        ),
        migrations.AlterModelTable(
            name='트로트entry',
            table='트로트_entry',
        ),
        migrations.AlterModelTable(
            name='해외 rbsoulentry',
            table='해외 RBSOUL_entry',
        ),
        migrations.AlterModelTable(
            name='해외 랩힙합entry',
            table='해외 랩힙합_entry',
        ),
        migrations.AlterModelTable(
            name='해외 록메탈entry',
            table='해외 록메탈_entry',
        ),
        migrations.AlterModelTable(
            name='해외 밴드entry',
            table='해외 밴드_entry',
        ),
        migrations.AlterModelTable(
            name='해외 포크블루스컨트리entry',
            table='해외 포크블루스컨트리_entry',
        ),
    ]
