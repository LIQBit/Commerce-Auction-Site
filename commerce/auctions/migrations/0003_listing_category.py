# Generated by Django 3.1 on 2020-09-15 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20200915_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('fashion', 'Fashion'), ('toys', 'Toys'), ('electronics', 'Electronics'), ('home', 'Home'), ('other', 'Other')], default=None, max_length=64),
        ),
    ]
