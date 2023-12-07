# Generated by Django 4.2.5 on 2023-12-07 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Onestop_App', '0014_appointment_admin_notification_sent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='appointment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='Onestop_App.appointment'),
        ),
    ]
