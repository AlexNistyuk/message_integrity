# Generated by Django 5.0.6 on 2024-06-25 17:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mails", "0003_alter_mail_received_date_alter_mail_sent_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mail",
            name="subject",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
