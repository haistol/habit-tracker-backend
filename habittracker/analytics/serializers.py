from rest_framework import serializers

from habits.models import Habit


class AnalyticHabitSerializer(serializers.ModelSerializer):
    periodicity = serializers.ChoiceField(choices=Habit.Period.choices, source='get_periodicity_display')

    class Meta:
        model = Habit
        fields = ['id', 'name', 'periodicity', 'created_at', 'is_active', 'streak']


class HabitLongestStreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'longest_streak']
