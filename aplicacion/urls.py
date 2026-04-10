from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('inicio/', views.inicio_view, name='inicio'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registrar/<int:partido_id>/', views.registrar_resultado, name='registrar_resultado'),
    path('reiniciar/', views.reiniciar_torneo, name='reiniciar_torneo'),
]