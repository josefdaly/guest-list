import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0013_event_marquee_banner_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='event',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
