# Generated by Django 4.2.2 on 2024-02-12 13:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('periodicity', models.IntegerField(choices=[(1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')], default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('streak', models.IntegerField(default=0)),
                ('longest_streak', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habits', related_query_name='habits', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Done'), (3, 'Past Due')], default=1)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', related_query_name='tasks', to='habits.habit')),
            ],
        ),
    ]
