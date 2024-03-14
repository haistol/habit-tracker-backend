from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import requests
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django import forms

from habits.models import Habit


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Store API authentication credentials in session
            request.session['api_username'] = username
            request.session['api_password'] = password
            # Redirect to a success page (e.g., home page)
            return redirect(reverse("index"))  # Assuming 'index' is the name of your homepage URL
        else:
            # Return an error message
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')


def index(request):
    if not request.session.get('api_username'):
        return redirect(reverse("login"))

    return render(request, 'index.html')


@login_required
def habits_list(request):
    # Use reverse to dynamically generate the URL
    api_url = request.build_absolute_uri(reverse('habit-list-api'))
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')

    response = requests.get(api_url, auth=(api_username, api_password))

    if response.status_code == 200:
        habits = response.json()
        return render(request, 'habits_list.html', {'habits': habits})
    else:
        # Handle error response
        return render(request, 'error.html', {'message': 'Failed to fetch habits data'})


@login_required
def habit_detail(request, habit_id):
    api_url = request.build_absolute_uri(reverse("habit-detail-api", kwargs={"id": habit_id}))
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')
    response = requests.get(api_url, auth=(api_username, api_password))

    if response.status_code == 200:
        habit = response.json()
        return render(request, 'habit_detail.html', {'habit': habit})
    else:
        # Handle error response
        return render(request, 'error.html', {'message': 'Failed to fetch habit details'})


class HabitUpdateForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'periodicity', 'is_active']

    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3

    PERIODICITY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]

    name = forms.CharField(label='Name', max_length=100)
    periodicity = forms.IntegerField(label='Periodicity', widget=forms.Select(choices=PERIODICITY_CHOICES))
    is_active = forms.BooleanField(label='Active', required=False)


@csrf_exempt
def habit_update(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        form = HabitUpdateForm(request.POST, instance=habit)
        if form.is_valid():
            # Prepare data to be sent to the API
            data = {
                'name': form.cleaned_data['name'],
                'periodicity': form.cleaned_data['periodicity'],
                'is_active': form.cleaned_data['is_active']
            }
            # Make a PUT request to the API endpoint
            api_url = request.build_absolute_uri(reverse("habit-update-api", kwargs={"id": habit_id}))
            api_username = request.session.get('api_username')
            api_password = request.session.get('api_password')
            response = requests.put(api_url, data=data, auth=(api_username, api_password))
            if response.status_code == 200:
                # Redirect to habit detail page upon successful update
                return redirect('habit-detail', habit_id=habit_id)
            else:
                # Handle API error response
                return render(request, 'error.html', {'message': 'Failed to update habit'})
    else:
        form = HabitUpdateForm(instance=habit)
    return render(request, 'habit_update.html', {'form': form})


@csrf_exempt
def habit_delete(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id)
    if request.method == 'POST':
        # Make a DELETE request to the API endpoint
        api_url = request.build_absolute_uri(reverse("habit-delete-api", kwargs={"id": habit_id}))
        api_username = request.session.get('api_username')
        api_password = request.session.get('api_password')
        response = requests.delete(api_url, auth=(api_username, api_password))
        if response.status_code == 204:
            # Redirect to habits list page upon successful deletion
            return redirect('habits-list')
        else:
            # Handle API error response
            return render(request, 'error.html', {'message': 'Failed to delete habit'})
    return render(request, 'habit_delete.html', {'habit': habit})


class HabitCreateForm(forms.Form):
    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3

    PERIODICITY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    ]

    name = forms.CharField(label='Name', max_length=100)
    periodicity = forms.IntegerField(label='Periodicity', widget=forms.Select(choices=PERIODICITY_CHOICES))
    is_active = forms.BooleanField(label='Active', required=False)


@csrf_exempt
def habit_create(request):
    if request.method == 'POST':
        form = HabitCreateForm(request.POST)
        if form.is_valid():
            # Prepare data to be sent to the API
            data = {
                'name': form.cleaned_data['name'],
                'periodicity': form.cleaned_data['periodicity'],
                'is_active': form.cleaned_data['is_active']
            }
            # Make a POST request to the API endpoint
            api_url = request.build_absolute_uri(reverse("habit-create-api"))

            api_username = request.session.get('api_username')
            api_password = request.session.get('api_password')
            response = requests.post(api_url, json=data, auth=(api_username, api_password))
            if response.status_code == 201:  # Assuming the API returns status code 201 for successful creation
                # Redirect to habits list page upon successful creation
                return redirect('habits-list')
            else:
                # Handle API error response
                return render(request, 'error.html', {'message': 'Failed to create habit'})
    else:
        form = HabitCreateForm()
    return render(request, 'habit_create.html', {'form': form})


def habit_analytics(request):
    # Get the periodicity parameter from the query string
    periodicity = request.GET.get('periodicity')

    # Construct the API endpoint URL with the periodicity parameter
    api_url = request.build_absolute_uri(reverse("analytics-habit-list-api"))
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')
    if periodicity:
        api_url += f'?periodicity={periodicity}'

    # Fetch data from the API endpoint
    response = requests.get(api_url, auth=(api_username, api_password))
    if response.status_code == 200:
        habits_analytics = response.json()
    else:
        # Handle API error response
        return render(request, 'error.html', {'message': 'Failed to fetch habit analytics'})

    # Pass data to the template
    return render(request, 'habit_analytics.html', {'habits_analytics': habits_analytics})


def longest_streak(request):
    # Get the habit_id parameter from the query string
    habit_id = request.GET.get('habit_id')

    # Construct the API endpoint URL with the filter parameter
    api_url = request.build_absolute_uri(reverse("analytics-habit-longest-streak-api"))
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')
    if habit_id:
        api_url += f'?habit_id={habit_id}'

    # Fetch data from the API endpoint
    response = requests.get(api_url,auth=(api_username, api_password))
    if response.status_code == 200:
        longest_streak_data = response.json()
    else:
        # Handle API error response
        return render(request, 'error.html', {'message': 'Failed to fetch longest streak data'})

    # Pass data to the template
    return render(request, 'longest_streak.html', {'longest_streak_data': longest_streak_data})
