# Generated by Django 2.1.7 on 2019-03-17 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_user_data_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='price_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult_price', models.IntegerField()),
                ('children_price', models.IntegerField()),
            ],
        ),
    ]