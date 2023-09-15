"""
URL configuration for habittracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from habits.views import HabitView, HabitsListView, HabitCreateView
from analytics.views import AnalyticsHabitsListView, HabitLongestStreakView

urlpatterns = [
    path('', lambda request: redirect('habits/')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('habits/', HabitsListView.as_view(), name='habit-list'),
    path('habit/<int:id>/', HabitView.as_view(http_method_names=['get']), name='habit-detail'),
    path('habit/<int:id>/update/', HabitView.as_view(http_method_names=['get','put']), name='habit-update'),
    path('habit/<int:id>/delete/', HabitView.as_view(http_method_names=['get','delete']), name='habit-delete'),
    path('habit/create/', HabitCreateView.as_view(), name='habit-create'),
    path('habit/<int:id>/task-complete/', HabitView.as_view(http_method_names=['post']), name='habit-task-complete'),
    path('analytics/habits/', AnalyticsHabitsListView.as_view(), name='analytics-habit-list'),
    path('analytics/habits/longest-streak/', HabitLongestStreakView.as_view(), name='analytics-habit-longest-streak'),

]
