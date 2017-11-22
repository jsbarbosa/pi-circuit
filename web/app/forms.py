from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

ELEMENTS = ['R%d'%(i+1) for i in range(5)]
ELEMENTS += ['LED']

SENSORS = ['adc%d'%i for i in range(4)]

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CircuitForm(forms.Form):
    for element in ELEMENTS:
        exec('%s = forms.BooleanField(required = False)'%element)
    for sensor in SENSORS:
        exec('%s = forms.BooleanField(required = False)'%sensor)
