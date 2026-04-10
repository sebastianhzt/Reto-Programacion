from django.urls import path
from .views import login_view, inicio_view

urlpatterns = [
    path('', login_view, name='login'),
    path('inicio/', inicio_view, name='inicio'),
]