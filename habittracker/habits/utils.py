from datetime import datetime, timedelta
from habits.models import Habit, TaskTracker


def create_habit_active_task(habit: Habit):
    """
    Create a task tracker for the given habit.
    The due date of the task tracker is based on the last task tracker of the habit.
    If the habit has no task tracker, the due date is set to today.

    :param habit: The habit for which to create a task tracker.
    """
    if habit.tasks.all().exists():
        base_date = habit.tasks.all().order_by('-due_date').first().due_date
    else:
        base_date = datetime.today()
    if datetime.today().date() < base_date:
        return

    due_date = base_date

    if habit.periodicity == Habit.Period.WEEKLY:
        due_date = due_date + timedelta(days=7)

    elif habit.periodicity == Habit.Period.MONTHLY:
        due_date = due_date + timedelta(days=30)

    TaskTracker.objects.create(habit=habit, due_date=due_date)


def check_task_past_due_date(task: TaskTracker) -> bool:
    """
    Check if the task is past due date and update the status.

    :param task: The task to check.
    :return: True if the task is past due date, False otherwise.
    """
    if task.due_date < datetime.today().date():
        task.status = TaskTracker.Status.PAST_DUE
        task.save()
        update_habit_streak(task)
        return True

    return False


def update_habit_streak(task: TaskTracker):
    """
    Update the streak of the habit.

    :param task: The current task tracker for the ending period of the habit.
    """
    if task.status == TaskTracker.Status.DONE:
        task.habit.streak += 1
        if task.habit.streak > task.habit.longest_streak:
            task.habit.longest_streak = task.habit.streak
    elif task.status == TaskTracker.Status.PAST_DUE:
        task.habit.streak = 0
    else:
        return

    task.habit.save()


def check_habits_for_active_task():
    """
    Check all habits for an active task. If a habit has no active task, create one.

    """
    for habit in Habit.objects.filter(is_active=True).all():

        if task := habit.tasks.filter(status=TaskTracker.Status.PENDING).first():
            if not check_task_past_due_date(task):
                continue

            create_habit_active_task(habit)

        else:
            create_habit_active_task(habit)
