# Generated by Django 4.2.5 on 2023-12-06 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onestop_App', '0012_ticket_admin_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Onestop_App.ticket'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
