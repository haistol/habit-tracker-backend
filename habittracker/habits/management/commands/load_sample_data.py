from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import transaction
from habits.models import Habit, TaskTracker

User = get_user_model()


def create_sample_habits():
    with transaction.atomic():
        user = User.objects.create_user(username='habit-user', password='habittest123')

        habit1 = Habit.objects.create(user=user, name='exercise', periodicity=Habit.Period.DAILY, streak=10,
                                      longest_streak=10)
        habit2 = Habit.objects.create(user=user, name='laundry', periodicity=Habit.Period.WEEKLY, streak=0,
                                      longest_streak=1)
        habit3 = Habit.objects.create(user=user, name='hiking', periodicity=Habit.Period.MONTHLY, streak=0,
                                      longest_streak=0)

        base_date = timezone.now()
        for i in range(10, 0, -1):
            due_date = base_date - timedelta(days=i)
            TaskTracker.objects.create(habit=habit1, due_date=due_date.date(), status=TaskTracker.Status.DONE,
                                       completed_at=due_date)
        TaskTracker.objects.create(habit=habit1, due_date=base_date.date(), status=TaskTracker.Status.PENDING)

        TaskTracker.objects.create(habit=habit2, due_date=base_date.date() - timedelta(days=10),
                                   status=TaskTracker.Status.DONE)
        TaskTracker.objects.create(habit=habit2, due_date=base_date.date() - timedelta(days=3),
                                   status=TaskTracker.Status.PAST_DUE)
        TaskTracker.objects.create(habit=habit2, due_date=base_date.date() + timedelta(days=4),
                                   status=TaskTracker.Status.PENDING)
        TaskTracker.objects.create(habit=habit3, due_date=base_date.date() + timedelta(days=20),
                                   status=TaskTracker.Status.PENDING)


class Command(BaseCommand):
    help = ("Check all active habits tasks due date and update their status. "
            "If a habit has no active task, create one.")

    def handle(self, *args, **options):
        create_sample_habits()
