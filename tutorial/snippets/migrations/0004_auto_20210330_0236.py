# Generated by Django 2.2 on 2021-03-30 02:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_reactionnetwork_reactionnetworks'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reactionnetworks',
            old_name='network_list',
            new_name='network',
        ),
        migrations.AddField(
            model_name='reactionnetworks',
            name='network_image',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reactionnetworks',
            name='network_text',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ReactionNetwork',
        ),
    ]