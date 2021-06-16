from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Vacation
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

def registration_process(request):  # processes the form data on the index.html page for creating a user
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')   # these are the error validations for the registration side of the form.
    else:
        # add a user to the database
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)  # these [''] will change
        request.session['logged_in'] = user.id  # the 'logged_in' variable here is created by me, as i create a session for the created user. This will be used in other defs as well
        return redirect('/dashboard')

def login_process(request):  # processes the form data on the index.html page for creating a user
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')  # These are the error validations for the login side of the form.
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = user.id # creating a session, naming that session whatever we want.
        return redirect('/dashboard')


def dashboard(request):  #landing page, aka the page you should see when you are logged in.
    if "logged_in" not in request.session: # AKA "If I'm not logged in..."
            return redirect('/')  # you will need these two lines in the other pages that you shouldn't be able to get to, except the login page.
    else:
        login = User.objects.get(id=request.session['logged_in'])  # The ID is gonna be the person that's logged in.
        context = {
            "logged_in": login,
            # 'user': User.objects.filter(email=request.session['logged_in']),
            # 'showtrips': Vacation.objects.filter(owner_of_trip=login)
            
        }
    return render(request, 'dashboard.html', context)  # ADD BACK THE CONTEXT 


def new_vacation(request):
    if "logged_in" not in request.session: # AKA "If I'm not logged in..."
        return redirect('/')
    else:
        return render(request, 'new_vacation.html')


def vacation_process(request):
    errors = Vacation.objects.vacation_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new_vacation')
    else:    
        loggedin_user = User.objects.get(id=request.session['logged_in']) # First, i have to get the user that i'm trying to add the new vacay to, so get their id, based on the session that was created for them.
        new_vacay = Vacation.objects.create(destination=request.POST['destination'], trip_start=request.POST['trip_start_date'], trip_end=request.POST['trip_end_date'], trip_plan=request.POST['trip_plan'], owner_of_trip=loggedin_user)  # this will associate the newly created vacation with the logged in user
        return redirect('/dashboard')

def edit_trip_process(request, id):
    errors = Vacation.objects.vacation_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_trip/{id}')
    else:
        trip_to_edit = Vacation.objects.get(id=id)
        trip_to_edit.destination = request.POST['destination']
        trip_to_edit.trip_start = request.POST['trip_start_date']
        trip_to_edit.trip_end = request.POST['trip_end_date']
        trip_to_edit.trip_plan = request.POST['trip_plan']
        trip_to_edit.save()
        return redirect('/dashboard')

def edit_trip(request, id):
    if "logged_in" not in request.session: # AKA "If I'm not logged in..."
        return redirect('/')
    else:
        context = {
            'trip_to_edit': Vacation.objects.get(id=id)
        }
        return render(request,'edit_trip.html', context)


def view_trip(request, id):
    if "logged_in" not in request.session: # AKA "If I'm not logged in..."
        return redirect('/')
    else:
        login = User.objects.get(id=request.session['logged_in'])
        context = {
            "logged_in": login,
            'view_trip': Vacation.objects.all().filter(id=id)
        }
        return render(request, 'view_trip.html', context)



def delete(request, id):
    trip = Vacation.objects.get(id=id)
    trip.delete()
    return redirect('/dashboard')

def logout(request): # Don't forget to create a button to logout.
    request.session.delete()
    return redirect('/')