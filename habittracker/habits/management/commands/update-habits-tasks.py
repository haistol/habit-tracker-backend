from django.core.management import BaseCommand

from habits.utils import check_habits_for_active_task


class Command(BaseCommand):
    help = ("Check all active habits tasks due date and update their status. "
            "If a habit has no active task, create one.")

    def handle(self, *args, **options):
        check_habits_for_active_task()
