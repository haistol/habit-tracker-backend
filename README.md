# Habit Tracker

## Description

This is a simple habit tracker that allows you to add habits and track them daily. This is the core implementation of
the app, and it is meant to be used as the backend for a mobile app.

## Getting Started

### Dependencies

* Python 3.7+
* Django 4.0+
* Django Rest Framework 3.12+

### Installing

* Clone the repository
* entry the project folder
* Install the dependencies: `pip install -r requirements.txt`
* Run the migrations: `python manage.py migrate`
* Create a superuser: `python manage.py createsuperuser`



### Executing program
The app is already configured to use sqlite database, so you don't need to configure anything else to run it.
To run the server, just run the following command in the root folder of the project:
```
python manage.py runserver
```
To run the tests, run the following command in the root folder of the project:
```
python manage.py test
```
To access the api, you can use the following urls (replace `<int:id>` with the id of the habit you want to see):

* for a list of your active habits:  http://localhost:8000/habits/
* to see one habit: http://localhost:8000/habit/<int:id>/
* to update some of the info of the habit: http://localhost:8000/habit/<int:id>/update/
* to delete the habit: http://localhost:8000/habit/<int:id>/delete/
* to create a new habit: http://localhost:8000/habit/create/
* to mark the current habit task as completed: http://localhost:8000/habit/<int:id>/task-complete/
* to see the habits with their current streak info: http://localhost:8000/analytics/habits/ also accepts an optional query parameter `?periodicity=[daily, weekly or monthly]` to filter the habits by their periodicity
* to see the habits longest streak: http://localhost:8000/analytics/habits/longest-streak/ also accepts an optional query parameter `?habit_id=<int:id>` to see the longest streak of a specific habit


**Note:** the urls are for local development, if you are using a different environment, you will need to change the url to match your environment.


