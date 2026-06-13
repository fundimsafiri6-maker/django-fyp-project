# Generated migration to add HOD role to User model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_emailverificationtoken_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                choices=[('student', 'Student'), ('staff', 'Staff'), ('hod', 'HOD'), ('admin', 'Admin')],
                max_length=10
            ),
        ),
    ]
