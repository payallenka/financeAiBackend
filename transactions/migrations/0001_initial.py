# Generated by Django 5.1.6 on 2025-02-13 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('category', models.CharField(choices=[('food', 'Food'), ('transport', 'Transport'), ('shopping', 'Shopping'), ('bills', 'Bills'), ('other', 'Other')], default='other', max_length=20)),
            ],
        ),
    ]
