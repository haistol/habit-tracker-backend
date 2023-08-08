from django.utils.timezone import now
from django.test import TestCase
from django.contrib.auth.models import User
from habits.models import Habit, TaskTracker


# TODO: Add tests for the following:
# - HabitTaskTrackerView


class HabitTestCase(TestCase):

    def setUp(self):
        pass

    def test_habit_view(self):
        """test thew habit view"""
        user = User.objects.create_user(username='testuser', password='12345')
        habit = Habit.objects.create(user=user, name='test habit', periodicity=Habit.Period.DAILY)
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]['name'], habit.name)
        self.assertEqual(data[0]['periodicity'], 'Daily')
        self.assertEqual(data[0]['is_active'], True)
        self.assertEqual(data[0]['current_period_due_date'], None)

    def test_habit_create_view(self):
        """test the habit create view"""
        user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/habit/create/', {'name': 'test habit', 'periodicity': Habit.Period.DAILY},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['name'], 'test habit')
        self.assertEqual(data['periodicity'], 'Daily')
        self.assertEqual(data['is_active'], True)
        self.assertEqual(data['current_period_due_date'], str(now().date()))

    def test_habit_update_view(self):
        """test the habit update view"""
        user = User.objects.create_user(username='testuser', password='12345')
        habit = Habit.objects.create(user=user, name='test habit', periodicity=Habit.Period.DAILY)
        self.client.login(username='testuser', password='12345')
        response = self.client.put(f'/habit/{habit.id}/update/',
                                   {'name': 'test habit updated', 'periodicity': Habit.Period.WEEKLY},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'test habit updated')
        self.assertEqual(data['periodicity'], 'Weekly')
        self.assertEqual(data['is_active'], True)
        self.assertEqual(data['current_period_due_date'], None)
