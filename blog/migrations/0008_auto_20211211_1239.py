# Generated by Django 3.1.4 on 2021-12-11 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_favourite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postpoint',
            name='post',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='post_post_points', to='blog.post', verbose_name='Пост этапа готовки'),
        ),
    ]