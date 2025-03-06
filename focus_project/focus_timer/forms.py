from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

from django import forms
from .models import Timers

class PomodoroForm(forms.ModelForm):
    class Meta:
        model = Timers
        fields = ['title','focus','rest','color']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 14, 'required': 'required'}),
            'focus': forms.NumberInput(attrs={'required': 'required', 'min': 0}),
            'rest': forms.NumberInput(attrs={'required': 'required', 'min': 0}),
            #'priority': forms.NumberInput(attrs={'required': 'required'}),
            'color': forms.NumberInput(attrs={'required': 'required', 'style': 'display: none;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        focus = cleaned_data.get('focus', 0)
        rest = cleaned_data.get('rest', 0)

        if focus < 0 or rest < 0:
            raise forms.ValidationError("Time must be non-negative.")
        '''
        # This if statement prevents timers longer than 60 minutes from being created
        if (focus + rest) > 60:
            raise forms.ValidationError("Total time cannot exceed 60 minutes.")
        '''
        return cleaned_data
