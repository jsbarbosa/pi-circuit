from django.shortcuts import render
from app.forms import NewUserForm, CircuitForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from queue import Queue, sleep
from numpy.random import random


queue = Queue(30)

ELEMENTS = ['R%d'%(i+1) for i in range(5)]
ELEMENTS += ['LED']

def index(request):
    return render(request, 'app/index.html')

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password = raw_password)
            login(request, user)

            return userpage(request)
    else:
        form = NewUserForm()
    return render(request, 'app/signup.html', context={'form': form})

def userlogout(request):
    logout(request)
    return index(request)

@login_required
def userpage(request):
    current_user = request.user
    if not queue.userInLine(current_user):
        queue.addUser(current_user)
        sleep(1)

    if queue.current_user == current_user:
        if request.method == 'POST':
            form = CircuitForm(request.POST)
            if form.is_valid():
                print(request.user)
                answers = [form.cleaned_data.get(element) for element in ELEMENTS]
                for i in range(len(ELEMENTS)):
                    print("%s: %s"%(ELEMENTS[i], answers[i]))
                return index(request)
        else:
            form =  CircuitForm()
        return render(request, 'app/userpage.html', context={'user': current_user, 'form': form})
    else:
        n, wait_time = queue.spectedTime(current_user)
        return render(request, 'app/line.html', context={'pos': n, 'left': wait_time})


@login_required
def userprofile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return userpage(request)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/userprofile.html', context={'form': form, 'user': request.user})
