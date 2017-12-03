from django.shortcuts import render, redirect
from app.forms import NewUserForm, OldCircuitForm, NewCircuitForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.conf import settings

from piCircuit import NADC, MAXVAL, digital

from queue import Queue, sleep
from numpy.random import random
from .port import PORT
queue = Queue(300)

class Measurement():
    def __init__(self, name, value):
        self.name = name
        if type(value) is int:
            self.value = "%d"%value
        elif type(value) is float:
            self.value = "%.3f"%value
        else:
            self.value = value

#~ ELEMENTS = ['R%d'%(i+1) for i in range(5)]
#~ ELEMENTS += ['LED']

ADC_TO_SHOW = []
OUT_TO_SHOW = []
IN_TO_SHOW = []
VREF = -1

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
    
def measurements(request):
    adc = []
    outs = []
    ins = []
    for item in ADC_TO_SHOW:
        name, i = item
        if name == "":
            name = "ADC%d"%i
        else:
            name += " (ADC%d)"%i
        value = PORT.getCurrentChannel(i)
        if VREF > 0:
            value *= VREF/MAXVAL
        m = Measurement(name, round(value, 3))
        adc.append(m)
        
    for item in OUT_TO_SHOW:
        name, i = item
        if name == "":
            name = "OUT%d"%i
        else:
            name += " (OUT%d)"%i
        digital.OUT_PINS[i].setState(1)
        m = Measurement(name, True)
        outs.append(m)
        
    for item in IN_TO_SHOW:
        name, i = item
        if name == "":
            name = "IN%d"%i
        else:
            name += " (IN%d)"%i
        val = digital.IN_PINS[i].getState()
        m = Measurement(name, bool(val))
        ins.append(m)
        
    return render(request, 'app/measurements.html', context={"adc_values": adc, "in_values": ins, "out_values": outs})

@login_required
def userpage(request):
    global ADC_TO_SHOW, IN_TO_SHOW, OUT_TO_SHOW, VREF
    
    current_user = request.user
    if not queue.userInLine(current_user):
        queue.addUser(current_user)
        sleep(1)

    if queue.current_user == current_user:
        if request.method == 'POST':
            form = NewCircuitForm(request.POST)
            form.split()
            if form.is_valid():
                """
                ADC
                """
                adc = form.ADC_PREFIX
                active = form.CHECKBOX_PREFIX + form.ADC_PREFIX
                vref = form.cleaned_data.get("Vref")
                try: vref = float(vref)
                except: vref = -1
                if vref > 0:
                    VREF = vref
                answers = [(form.cleaned_data.get("%s%d"%(active, i)), 
                                form.cleaned_data.get("%s%d"%(adc, i))) for i in range(NADC)]
                ADC_TO_SHOW = []

                for i, ans in enumerate(answers):
                    if ans[0]:
                        ADC_TO_SHOW.append((ans[1], i))
                        
                """
                OUTS
                """
                outs = form.OUT_PREFIX
                active = form.CHECKBOX_PREFIX + form.OUT_PREFIX
                answers = [(form.cleaned_data.get("%s%d"%(active, i)), 
                                form.cleaned_data.get("%s%d"%(outs, i))) for i in range(form.NOUT)]
                OUT_TO_SHOW = []

                for i, ans in enumerate(answers):
                    if ans[0]:
                        OUT_TO_SHOW.append((ans[1], i))
                        
                """
                INS
                """
                ins = form.IN_PREFIX
                active = form.CHECKBOX_PREFIX + form.IN_PREFIX
                answers = [(form.cleaned_data.get("%s%d"%(active, i)), 
                                form.cleaned_data.get("%s%d"%(ins, i))) for i in range(form.NIN)]
                                
                IN_TO_SHOW = []

                for i, ans in enumerate(answers):
                    if ans[0]:
                        IN_TO_SHOW.append((ans[1], i))                        
                return measurements(request)
        else:
            ADC_TO_SHOW = []
            OUT_TO_SHOW = []
            IN_TO_SHOW = []
            VREF = -1
            form = NewCircuitForm().split()
            vref, adc, outs, ins = form 
        return render(request, 'app/userpage.html', context={'user': current_user,
                    'vref': vref, 'adc': adc, 'ins': ins, 'outs': outs})
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
