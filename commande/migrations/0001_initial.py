# Generated by Django 4.2.5 on 2024-11-06 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Livré', 'Livré'), ('Non livré', 'Non livré'), ('En instance', 'En instance'), ('Soumis', 'Soumis'), ('Non soumis', 'Non soumis')], default='Non soumis', max_length=200, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='client.client')),
            ],
        ),
    ]