from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_add_performance_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='location',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='university',
            name='website',
            field=models.URLField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='university',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='university',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='university',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='university',
            name='rector_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
