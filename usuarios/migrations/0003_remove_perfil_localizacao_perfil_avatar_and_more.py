# Generated by Django 5.1.6 on 2025-02-25 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_perfil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='localizacao',
        ),
        migrations.AddField(
            model_name='perfil',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='perfil',
            name='cidade',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='estado',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(null=True),
        ),
    ]
