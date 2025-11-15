# Generated manually for TZ refactoring

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adverts', '0002_mediaasset_duration_mediaasset_media_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediaasset',
            old_name='media_type',
            new_name='type',
        ),
        # upload_to будет изменен в следующей миграции на функцию
        migrations.AddField(
            model_name='mediaasset',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Ширина (для изображений)'),
        ),
        migrations.AddField(
            model_name='mediaasset',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Высота (для изображений)'),
        ),
        migrations.AddField(
            model_name='mediaasset',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='adverts/%Y/%m/', verbose_name='Постер (для видео)'),
        ),
        migrations.AlterField(
            model_name='mediaasset',
            name='size',
            field=models.PositiveIntegerField(default=0, verbose_name='Размер (байт)'),
        ),
    ]

