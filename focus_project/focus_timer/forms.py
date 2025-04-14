from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import CustomUser, Timers, Themes

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

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

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Themes
        fields = ['title', 'color1', 'color2', 'color3', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'maxlength': 14, 'required': 'required'}),
            'color1': forms.TextInput(attrs={'type': 'color'}),
            'color2': forms.TextInput(attrs={'type': 'color'}),
            'color3': forms.TextInput(attrs={'type': 'color'}),
            'image': forms.ClearableFileInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['color1', 'color2', 'color3']:
            value = cleaned_data.get(field)
            if value:
                cleaned_data[field] = value.strip()
        return cleaned_data