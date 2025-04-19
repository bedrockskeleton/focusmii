from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
from .models import CustomUser, Timers, Themes
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

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
        
        return cleaned_data
    
# Profile Forms

User = get_user_model()

class CustomUsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'})
        }
        
class CustomEmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

# Theme Forms

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Themes
        fields = ['title', 'color1', 'color2', 'color3', 'image']
        labels = {'title':'Title',
                  'color1':'',
                  'color2':'',
                  'color3':'',
                  'image':'Image'}
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