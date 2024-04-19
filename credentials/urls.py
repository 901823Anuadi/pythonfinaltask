from django.urls import path
from . import views

app_name="credentials"

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.my_view, name="my_view"),

]