ffrom django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Equipo, Partido



def dashboard(request):
    # Obtener equipos ordenados por puntos y diferencia de goles
    equipos = list(Equipo.objects.all())
    equipos.sort(key=lambda x: (x.puntos, x.diferencia_goles, x.goles_a_favor), reverse=True)
    
    partidos = Partido.objects.all()
    
    # Si no hay partidos, generarlos automáticamente (Round Robin)
    if not partidos.exists():
        # generar_enfrentamientos()
        partidos = Partido.objects.all()
        
    return render(request, 'torneo/dashboard.html', {
        'equipos': equipos,
        'partidos': partidos
    })


def registrar_resultado(request, partido_id):
    if request.method == 'POST':
        partido = get_object_or_404(Partido, id=partido_id)
        if not partido.jugado:
            try:
                goles_l = int(request.POST.get('goles_local', 0))
                goles_v = int(request.POST.get('goles_visitante', 0))
                
                partido.goles_local = goles_l
                partido.goles_visitante = goles_v
                partido.jugado = True
                partido.save()
                
                # Actualizar estadísticas de equipos
                actualizar_estadisticas(partido.equipo_local, goles_l, goles_v)
                actualizar_estadisticas(partido.equipo_visitante, goles_v, goles_l)
            except ValueError:
                pass # Manejar error de entrada no numérica si es necesario
            
    return redirect('dashboard')

def actualizar_estadisticas(equipo, goles_f, goles_c):
    equipo.partidos_jugados += 1
    equipo.goles_a_favor += goles_f
    equipo.goles_en_contra += goles_c
    
    if goles_f > goles_c:
        equipo.victorias += 1
        equipo.puntos += 3
    elif goles_f == goles_c:
        equipo.empates += 1
        equipo.puntos += 1
    else:
        equipo.derrotas += 1
        
    equipo.save()


def reiniciar_torneo(request):
    # Reiniciar estadísticas de equipos
    Equipo.objects.all().update(
        puntos=0,
        partidos_jugados=0,
        victorias=0,
        empates=0,
        derrotas=0,
        goles_a_favor=0,
        goles_en_contra=0
    )
    # Eliminar partidos para que se vuelvan a generar
    Partido.objects.all().delete()
    return redirect('dashboard')
