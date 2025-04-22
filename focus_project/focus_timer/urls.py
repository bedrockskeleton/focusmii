from django.urls import path
from focus_timer import views

urlpatterns = [
    path('', views.pomodoro_timer, name='pomodoro_timer'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('add/<int:id>', views.add, name="add"),
    path('delete/<str:id>/', views.delete, name="delete"),
    # Profile Management
    path('profile', views.profile, name='profile'),
    # Theme URLs
    path('themes/', views.themes, name='themes'),
    path('themes/add/', views.themes_add, name='themes_add'),
    path('themes/edit/<int:theme_id>', views.themes_edit, name='themes_edit'),
    path('themes/delete/<int:theme_id>/', views.themes_delete, name='themes_delete'),
    path('themes/set/<int:theme_id>/', views.themes_set, name='themes_set'),
    path('themes/default/', views.themes_default, name='themes_default'),
    # Calcuation URLs
    path('calculations/', views.calculations, name='calculations'),
]
