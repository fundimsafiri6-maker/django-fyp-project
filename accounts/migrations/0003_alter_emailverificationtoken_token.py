# Migration to fix MySQL compatibility issue with token field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_email_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverificationtoken',
            name='token',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
