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
from habits.views import HabitView, HabitsListView, HabitCreateView
from analytics.views import AnalyticsHabitsListView, HabitLongestStreakView
from frontend.views import user_login, habits_list, habit_detail, habit_update, habit_delete, habit_create, \
    habit_analytics, index, longest_streak

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('habits/', habits_list, name='habits-list'),
    path('admin/', admin.site.urls),
    path('habits/<int:habit_id>/', habit_detail, name='habit-detail'),
    path('habits/<int:habit_id>/update/', habit_update, name='habit-update'),
    path('habits/<int:habit_id>/delete/', habit_delete, name='habit-delete'),
    path('habits/create/', habit_create, name='habit-create'),
    path('analytics/habits/', habit_analytics, name='habit-analytics'),
    path('analytics/habits/longest-streak/', longest_streak, name='longest-streak'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/habits/', HabitsListView.as_view(), name='habit-list-api'),
    path('api/habit/<int:id>/', HabitView.as_view(http_method_names=['get']), name='habit-detail-api'),
    path('api/habit/<int:id>/update/', HabitView.as_view(http_method_names=['get', 'put']), name='habit-update-api'),
    path('api/habit/<int:id>/delete/', HabitView.as_view(http_method_names=['get', 'delete']), name='habit-delete-api'),
    path('api/habit/create/', HabitCreateView.as_view(), name='habit-create-api'),
    path('api/habit/<int:id>/task-complete/', HabitView.as_view(http_method_names=['post']),
         name='habit-task-complete'),
    path('api/analytics/habits/', AnalyticsHabitsListView.as_view(), name='analytics-habit-list-api'),
    path('api/analytics/habits/longest-streak/', HabitLongestStreakView.as_view(),
         name='analytics-habit-longest-streak-api'),

]
