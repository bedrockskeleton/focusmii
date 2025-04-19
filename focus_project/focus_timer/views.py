from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash
# Model imports
from .models import Timers, Themes
User = get_user_model()
from django.contrib import auth, messages
# Form imports
from .forms import PomodoroForm, CustomUsernameChangeForm, CustomEmailChangeForm, CustomPasswordChangeForm, ThemeForm
from django.contrib.auth.forms import PasswordChangeForm
# Importing my theme utility from utils.py
from .utils import get_selected_theme

def pomodoro_timer(request):
    form = PomodoroForm()
    timers = []
    theme = get_selected_theme(request.user)
    if request.user.is_authenticated:
        timers = Timers.objects.all().order_by('priority')
    
    if len(timers) == 0:
        return render(request, 'pomodoro_timer.html', {
            'form': form,
            'current_theme': theme,
            'editable': False,
            'timers': None,
        })
    
    return render(request, 'pomodoro_timer.html', {
        'form': form,
        'current_theme': theme,
        'editable': False,
        'timers': timers,
    })

def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('pomodoro_timer')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect("login")
        else:
            messages.info(request, "Invalid email or password")
            return redirect('login')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        '''
        # Unique usernames depricated, accounts now only need email to be unique
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('signup')
        '''
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            return redirect('login')
    else:
        return render(request, 'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('pomodoro_timer')

def add(request,id):
    if request.method == "POST":
        form = PomodoroForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.uuid = id
            form_instance.save()
            return redirect("pomodoro_timer")
    else:
        form = PomodoroForm()
        timers = Timers.objects.all()
        current_theme = get_selected_theme(request.user)
        return render(request, 'pomodoro_timer.html', {
            'form': form,
            'timers': timers,
            "editable": True,
            "current_theme": current_theme
        })

def delete(request, id):
    try:
        timers = Timers.objects.get(id=id)
        timers.delete()
        timers = Timers.objects.all()
        form = PomodoroForm()
        return redirect('pomodoro_timer')
        '''if len(timers) == 0:
            return render(request, 'pomodoro_timer.html', {
                'form': form,
                "editable": False,
                'timers': None
            })
        return render(request, 'pomodoro_timer.html', {
            'form': form,
            "editable": False,
            'timers': timers
        })'''
    except Timers.DoesNotExist:
        return redirect('pomodoro_timer')

# View for profile

def profile(request):
    user = request.user
    username_form = CustomUsernameChangeForm(instance=user)
    email_form = CustomEmailChangeForm(instance=user)
    password_form = CustomPasswordChangeForm(user)
    current_theme = get_selected_theme(user)

    if user.is_authenticated:
        if request.method == 'POST':
            if 'change_username' in request.POST:
                username_form = CustomUsernameChangeForm(request.POST, instance=user)
                if username_form.is_valid():
                    username_form.save()
            elif 'change_email' in request.POST:
                email_form = CustomEmailChangeForm(request.POST, instance=user)
                if User.objects.filter(email=request.POST['email']).exists():
                    messages.info(request, "Email already taken")
                    return redirect('profile')
                if email_form.is_valid():
                    email_form.save()
                    return redirect('profile')
            elif 'change_password' in request.POST:
                password_form = CustomPasswordChangeForm(user, request.POST)
                if password_form.is_valid():
                    password_form.save()
                    update_session_auth_hash(request, password_form.user)  # Prevents logout
            elif 'delete_timers' in request.POST:
                Timers.objects.filter(uuid=user.id).delete()
            elif 'delete_themes' in request.POST:
                user.current_theme = None
                Themes.objects.filter(user=user).delete()
            elif 'delete_profile' in request.POST:
                Timers.objects.filter(uuid=user.id).delete()
                Themes.objects.filter(user=user).delete() # Doing this just to clear images out of uploads/themes
                user.delete()
                return redirect('pomodoro_timer')

            return redirect('profile')
        else:
            return render(request, 'profile.html', {
                'user': user,
                'current_theme': current_theme,
                'username_form': username_form,
                'email_form': email_form,
                'password_form': password_form,
            })
    else:
        return redirect('pomodoro_timer')

# Views for themes

def themes(request):
    themes = request.user.themes.all()
    form = ThemeForm()
    theme = get_selected_theme(request.user)
    if request.user.is_authenticated:
        return render(request, 'themes.html', {
            'themes': themes,
            'form': form,
            'current_theme': theme,
            'editable': False
        })
    else:
        return redirect('pomodoro_timer')

def themes_add(request):
    editable = True  # Show form by default for GET
    user = request.user
    current_theme = get_selected_theme(user)
    
    if request.user.is_authenticated:
        if request.method == "POST":
            editable = False  # Hide form after submitting
            form = ThemeForm(request.POST, request.FILES)
            if form.is_valid():
                theme = form.save(commit=False)
                theme.user = user
                for color in [theme.color2, theme.color3]:
                    if color == "#000000":
                        color = None
                theme.save()
                return redirect("themes")
        else:
            form = ThemeForm()
    else:
        return redirect('pomodoro_timer') # Take users back to the home page if they're not logged in

    themes = user.themes.all()
    return render(request, 'themes.html', {
        'form': form,
        'editable': editable,
        'themes': themes,
        'current_theme': current_theme,
    })

def themes_edit(request, theme_id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Themes, id=theme_id, user=request.user)
        if request.method == 'POST':
            form = ThemeForm(request.POST, request.FILES, instance=theme)
            if form.is_valid():
                form.save()
                return redirect('themes')
        else:
            form = ThemeForm(instance=theme)

        return render(request, 'edit_theme.html', {'form': form, 'theme': theme})
    else:
        return redirect('themes')

def themes_delete(request, theme_id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Themes, id=theme_id, user=request.user)
        if request.method == 'POST':
            if request.user.profile.selected_theme == theme:
                try:
                    request.user.profile.selected_theme = None  # Clear current theme if it's being deleted
                except AttributeError:
                    pass
                request.user.profile.save()
            image = theme.image
            image.delete() # Remove the image (if applicable) from the uploads directory
            theme.delete() # Now I can safely delete the whole theme
    return redirect('themes')

def themes_set(request, theme_id):
    if request.user.is_authenticated:
        theme = get_object_or_404(Themes, id=theme_id)
        request.user.profile.selected_theme = theme
        request.user.profile.save()
        return redirect('themes')
    else:
        return redirect('pomodoro_timer')
    
def themes_default(request):
    if request.user.is_authenticated:
        request.user.profile.selected_theme = None
        request.user.profile.save()
        return redirect('themes')
    else:
        return redirect('pomodoro_timer')