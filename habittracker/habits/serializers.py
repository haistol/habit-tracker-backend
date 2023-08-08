from django.contrib.auth.models import User
from rest_framework import serializers

from habits.models import Habit, TaskTracker


class HabitSerializer(serializers.ModelSerializer):
    current_period_due_date = serializers.SerializerMethodField()
    periodicity = serializers.ChoiceField(choices=Habit.Period.choices, source='get_periodicity_display')

    class Meta:
        model = Habit
        fields = ['id', 'name', 'periodicity', 'created_at', 'is_active', 'current_period_due_date']

    def get_current_period_due_date(self, obj):
        if task := obj.tasks.filter(status=TaskTracker.Status.PENDING).first():
            return task.due_date

        return None

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.periodicity = validated_data.get('periodicity', instance.periodicity)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class HabitUpdateSerializer(serializers.ModelSerializer):
    periodicity = serializers.ChoiceField(choices=Habit.Period.choices)

    class Meta:
        model = Habit
        fields = ['id', 'name', 'periodicity', 'is_active']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.periodicity = validated_data.get('periodicity', instance.periodicity)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance


class HabitCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'periodicity']

    periodicity = serializers.ChoiceField(choices=Habit.Period.choices)

    def create(self, validated_data):
        user = self.context['request'].user
        habit = Habit.objects.create(user=user, **validated_data)
        return habit
