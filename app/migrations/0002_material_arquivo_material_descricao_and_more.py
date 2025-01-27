# Generated by Django 5.1.5 on 2025-01-27 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='arquivo',
            field=models.FileField(default='materiais/exemplo.pdf', upload_to='materiais/'),
        ),
        migrations.AddField(
            model_name='material',
            name='descricao',
            field=models.TextField(default='Sem descrição'),
        ),
        migrations.AlterField(
            model_name='material',
            name='autor',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='material',
            name='tipo',
            field=models.CharField(choices=[('SL', 'Slide'), ('VD', 'Vídeo'), ('DC', 'Documento')], default='DC', max_length=2),
        ),
        migrations.AlterField(
            model_name='material',
            name='titulo',
            field=models.CharField(max_length=200),
        ),
    ]
