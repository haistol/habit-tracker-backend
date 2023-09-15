from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView

from habits.models import Habit, TaskTracker
from analytics.serializers import AnalyticHabitSerializer, HabitLongestStreakSerializer


class AnalyticsHabitsListView(ListAPIView):
    """A view to list all the user active habits with their analytics, filtered by periodicity"""
    serializer_class = AnalyticHabitSerializer

    def get_queryset(self):
        user = self.request.user
        periodicity = self.request.query_params.get('periodicity', None)
        if periodicity and periodicity.upper() in Habit.Period.__members__:
            return Habit.objects.filter(user=user, is_active=True, periodicity=Habit.Period[periodicity.upper()])
        if periodicity and not periodicity.upper() in Habit.Period.__members__:
            raise ValueError(f"Periodicity '{periodicity}' is not valid")

        return Habit.objects.filter(user=user, is_active=True)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response(data)


class HabitLongestStreakView(RetrieveAPIView):
    """A view for habits longest streak. If habit_id is passed, it will return the longest streak for that habit only"""
    serializer_class = HabitLongestStreakSerializer

    def get_queryset(self):
        user = self.request.user
        habit_id = self.request.query_params.get('habit_id', None)
        if habit_id:
            return Habit.objects.filter(user=user, is_active=True, id=habit_id)

        return Habit.objects.filter(user=user, is_active=True)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_queryset()
        serializer = HabitLongestStreakSerializer(instance, many=True)
        return Response(serializer.data)
