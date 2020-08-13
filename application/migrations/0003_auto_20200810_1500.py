# Generated by Django 3.1 on 2020-08-10 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20200810_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historique',
            name='primary_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_primary_manual_roats', to=settings.AUTH_USER_MODEL, verbose_name='First Player'),
        ),
        migrations.AlterField(
            model_name='historique',
            name='secondary_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_secondary_manual_roats', to=settings.AUTH_USER_MODEL, verbose_name='Second Player'),
        ),
    ]
