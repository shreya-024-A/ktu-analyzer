from django.urls import path
from . import views

urlpatterns = [
    path('', views.your_view_name, name='home'),
]