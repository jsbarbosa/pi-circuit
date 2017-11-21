from django import forms
from app.models import User

class NewUserForm(forms.ModelForm):
    class Meta():
        model = User
        widgets = {'password': forms.PasswordInput()}
        fields = '__all__'
