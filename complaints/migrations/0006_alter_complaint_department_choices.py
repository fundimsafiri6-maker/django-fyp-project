from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0005_alter_complaint_options_complaint_ai_classified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='department',
            field=models.CharField(blank=True, choices=[('academic', 'Academic'), ('ict', 'ICT'), ('other', 'Other')], help_text='Department this complaint is routed to', max_length=20, null=True),
        ),
    ]