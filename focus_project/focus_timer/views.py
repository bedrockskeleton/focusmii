from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Timers, Themes
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import auth, messages
from .forms import PomodoroForm, ThemeForm
from django.db.models import Sum, F, ExpressionWrapper, fields
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
        if User.objects.filter(username=email).exists():
            user = auth.authenticate(username=email, password=password)
            print(user)
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
        name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(first_name=name).exists():
            messages.info(request, "Username already taken")
            return redirect('signup')
        elif User.objects.filter(username=email).exists():
            messages.info(request, "Email already taken")
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name=name,
                                            username=email,
                                            password=password)
            print(user)
            print("User registered Successfully")
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
        print(f'Successfully Deleted {id}')
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
    
'''def themes_add(request):
    if request.method == 'POST':
        form = ThemeForm(request.POST, request.FILES)
        if form.is_valid():
            theme = form.save(commit=False)
            theme.user = request.user
            theme.save()
    return render(request, 'themes.html', {
        'themes': themes
        'form': form,
        'current_theme'
    })''' # Redirect back to themes whether the request was a POST or not

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
                    print(type(color), color)
                    if color == "#000000":
                        color = None
                    print(type(color), color)
                print(theme.color3)
                theme.save()
                return redirect("themes")
            else:
                print("theme form not valid")
                print(form.errors)
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
    print("user authenticated?", request.user.is_authenticated)
    if request.user.is_authenticated:
        print("request method?", request.method)
        theme = get_object_or_404(Themes, id=theme_id, user=request.user)
        if request.method == 'POST':
            print("posting delete...")
            if request.user.profile.selected_theme == theme:
                print("deleting selected theme...")
                try:
                    request.user.profile.selected_theme = None  # Clear current theme if it's being deleted
                except AttributeError:
                    pass
                request.user.profile.save()
            print(f'deleting theme {theme.id}...')
            theme.delete()
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