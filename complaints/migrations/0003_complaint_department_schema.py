# Empty migration - database schema already contains all fields
# This migration stores the migration history point

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_complaint_assigned_to_complaintresponse'),
    ]

    operations = [
    ]
