# Generated by Django 5.1.6 on 2025-03-03 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_student_matricule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='matricule',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
