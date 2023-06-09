from datetime import datetime, timedelta
from habits.models import Habit, TaskTracker


def create_habit_active_task(habit):
    """Create a task tracker for the given habit."""
    if habit.tasks.all().exists():
        base_date = habit.tasks.all().order_by('-due_date').first().due_date
    else:
        base_date = datetime.today()

    if habit.periodicity == Habit.Period.DAILY:
        task_tracker = TaskTracker.objects.create(habit=habit, due_date=base_date)
    elif habit.periodicity == Habit.Period.WEEKLY:
        task_tracker = TaskTracker.objects.create(habit=habit, due_date=base_date + timedelta(days=7))
    elif habit.periodicity == Habit.Period.MONTHLY:
        task_tracker = TaskTracker.objects.create(habit=habit, due_date=base_date + timedelta(days=30))

    return task_tracker
