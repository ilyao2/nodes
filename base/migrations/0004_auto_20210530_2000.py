# Generated by Django 3.2.3 on 2021-05-30 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='Title',
        ),
        migrations.RemoveField(
            model_name='node',
            name='Content',
        ),
        migrations.AddField(
            model_name='content',
            name='Node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.node'),
        ),
        migrations.AddField(
            model_name='node',
            name='Title',
            field=models.CharField(default='Node Title', max_length=150, verbose_name='Title'),
            preserve_default=False,
        ),
    ]
