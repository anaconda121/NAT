# Generated by Django 3.1.2 on 2021-02-07 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0007_patientdemographic_mrn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PatientID', models.IntegerField(blank=True, null=True)),
                ('TimelineDTS', models.DateField(blank=True, null=True)),
                ('TimelineValue', models.TextField(blank=True, null=True)),
                ('EventType', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='SpecialtyDSC',
            field=models.TextField(blank=True, null=True),
        ),
    ]