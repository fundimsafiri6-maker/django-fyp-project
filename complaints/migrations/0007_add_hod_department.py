# Generated migration to add HOD department choice

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0006_alter_complaint_department_choices'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='department',
            field=models.CharField(
                blank=True,
                choices=[('academic', 'Academic'), ('ict', 'ICT'), ('hod', 'HOD'), ('other', 'Other')],
                help_text='Department this complaint is routed to',
                max_length=20,
                null=True
            ),
        ),
    ]
