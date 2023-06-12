from django.db import models
from django.contrib.auth.models import User


class Habit(models.Model):
    """A model to represent a habit."""

    class Period(models.IntegerChoices):
        DAILY = 1
        WEEKLY = 2
        MONTHLY = 3

    name = models.CharField(max_length=200)
    periodicity = models.IntegerField(choices=Period.choices, default=Period.DAILY)
    user = models.ForeignKey(User, related_name="habits", related_query_name="habits", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def to_representation(self, instance):
        """Custom representation for the habit model."""
        representation = super().to_representation(instance)
        representation['periodicity'] = Habit.Period(representation['periodicity']).label
        return representation


class TaskTracker(models.Model):
    """A model to track the completion of a habit on a given date."""
    habit = models.ForeignKey(Habit, related_name="tasks", related_query_name="tasks", on_delete=models.CASCADE)
    due_date = models.DateField()
    done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.habit.name} - {self.date}'

    @property
    def done_on_time(self):
        return self.completed_at.date() <= self.due_date
