from django.urls import path
from . import views

urlpatterns=[
path("", views.login_view, name="root"),
    path('logout', views.logout, name='logout'),
    path('home/',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('verify/',views.verify_otp,name='verify'),
]