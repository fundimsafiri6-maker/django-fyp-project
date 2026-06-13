# Generated migration to add updated_at field to Complaint model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0003_complaint_department_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
