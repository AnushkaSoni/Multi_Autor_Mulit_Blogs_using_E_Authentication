# Generated by Django 3.2.4 on 2021-07-13 07:41

# import ckeditor.fields
from django.db import migrations,models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210713_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
