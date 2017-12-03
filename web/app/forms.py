from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from piCircuit import NADC, digital, exampleCircuit

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ExampleCircuitForm(forms.Form):
	choices1 = (
    ('1', "R = 100 Ω"),
    ('2', "Open circuit"),
    ('3', 'R = 2200 Ω'),
    ('4', 'Wire'),)
    
	choices2 = (
    ('1', "R = 220 Ω"),
    ('2', "Open circuit"),
    ('3', 'R = 33000 Ω'),
    ('4', 'Wire'),)
    
	E1 = forms.ChoiceField(choices=choices1)
	E2 = forms.ChoiceField(choices=choices1)
	E3 = forms.ChoiceField(choices=choices2)
	E4 = forms.ChoiceField(choices=choices2)
        
class NewCircuitForm(forms.Form):
	ADC_FIELDS = 2
	ADC_PREFIX = "ADC"
	
	IN_FIELDS = 2
	IN_PREFIX = "IN"
	
	OUT_FIELDS = 2
	OUT_PREFIX = "OUT"
	CHECKBOX_PREFIX = "Active"
	
	NOUT = len(digital.OUT_PINS)
	NIN = len(digital.IN_PINS)
	
	for i in range(NADC):
		Vref = forms.CharField(required = False)
		exec("%s%d = forms.CharField(required = False)"%(ADC_PREFIX, i))
		exec("%s%s%d = forms.BooleanField(required = False)"%(CHECKBOX_PREFIX, ADC_PREFIX, i))
		
	for i in range(NOUT):
		exec("%s%d = forms.CharField(required = False)"%(OUT_PREFIX, i))
		exec("%s%s%d = forms.BooleanField(required = False)"%(CHECKBOX_PREFIX, OUT_PREFIX, i))
	
	for i in range(NIN):
		exec("%s%d = forms.CharField(required = False)"%(IN_PREFIX, i))
		exec("%s%s%d = forms.BooleanField(required = False)"%(CHECKBOX_PREFIX, IN_PREFIX, i))
		
	def split(self):
		temp = []
		inner = []
		ADCS = []
		OUTS = []
		INS = []
		
		nadcs = self.ADC_FIELDS * NADC
		nouts = self.OUT_FIELDS * self.NOUT
		nins = self.IN_FIELDS * self.NIN
		for (i, field) in enumerate(self):
			if i == 0:
				temp.append(field)
			elif i < nadcs + 1:
				j = (i - 1)%self.ADC_FIELDS
				if j%2 == 0:
					inner.append(field.name)
					inner.append(field)
				else:
					inner.append(field)
					ADCS.append(inner)
					inner = []
			elif i < nouts + nadcs + 1:
				j = (i - 1 - nadcs)%self.OUT_FIELDS
				if j%2 == 0:
					inner.append(field.name)
					inner.append(field)
				else:
					inner.append(field)
					OUTS.append(inner)
					inner = []
				digital.OUT_PINS[j].setState(0)
			elif i < nins + nouts + nadcs + 1:
				j = (i - 1 - nouts - nadcs)%self.IN_FIELDS
				if j%2 == 0:
					inner.append(field.name)
					inner.append(field)
				else:
					inner.append(field)
					INS.append(inner)
					inner = []
		temp.append(ADCS)
		temp.append(OUTS)
		temp.append(INS)
		return temp
					
			
