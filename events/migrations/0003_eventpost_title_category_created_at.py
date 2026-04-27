import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_eventpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpost',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventpost',
            name='category',
            field=models.CharField(
                choices=[
                    ('Life', 'Life'),
                    ('News', 'News'),
                    ('Parties', 'Parties'),
                    ('Music', 'Music'),
                    ('Rants', 'Rants'),
                    ('Other', 'Other'),
                ],
                default='Other',
                max_length=50,
            ),
        ),
        migrations.AddField(
            model_name='eventpost',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='eventpost',
            options={'ordering': ['-created_at']},
        ),
    ]
