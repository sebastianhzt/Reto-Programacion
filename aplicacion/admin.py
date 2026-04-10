from django.contrib import admin
from .models import Equipo, Partido


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntos', 'partidos_jugados', 'victorias', 'empates', 'derrotas')


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('equipo_local', 'equipo_visitante', 'goles_local', 'goles_visitante', 'jugado')
