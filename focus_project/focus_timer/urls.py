from django.urls import path
from focus_timer import views

urlpatterns = [
    path('', views.pomodoro_timer, name='pomodoro_timer'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('add/<int:id>', views.add, name="add"),
    path('delete/<str:id>/', views.delete, name="delete"),
]
