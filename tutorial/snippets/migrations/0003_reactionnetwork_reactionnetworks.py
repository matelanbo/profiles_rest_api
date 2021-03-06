# Generated by Django 2.2 on 2021-03-30 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0002_auto_20210329_2203'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReactionNetworks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('network_list', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ReactionNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.ReactionNetworks')),
            ],
        ),
    ]
