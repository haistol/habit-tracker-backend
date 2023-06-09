from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from habits.models import Habit, TaskTracker

from habits.serializers import HabitSerializer, HabitCreateSerializer
from habits.utils import create_habit_active_task


class HabitView(RetrieveUpdateDestroyAPIView):
    """A viewset for viewing habits."""
    queryset = Habit.objects.all()
    lookup_field = "id"
    serializer_class = HabitSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        habit = self.get_object()
        serializer = HabitSerializer(habit, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class HabitsListView(ListAPIView):
    """A viewset for viewing habits."""
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitCreateView(CreateAPIView):
    """A viewset for creating habits."""
    serializer_class = HabitCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = HabitCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        habit = serializer.save()
        create_habit_active_task(habit)
        return Response(HabitCreateSerializer(habit).data)

class HabitTaskTrackerView(RetrieveAPIView):
    """A viewset for viewing habits."""
    queryset = TaskTracker.objects.all()
    lookup_field = "id"
    serializer_class = HabitSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = HabitSerializer(instance)
        return Response(serializer.data)