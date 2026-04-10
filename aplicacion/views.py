
from itertools import combinations

from django.shortcuts import get_object_or_404, redirect, render

from .models import Equipo, Partido

EQUIPOS_BASE = ['PSG', 'BAYER', 'ATHLETIC', 'CHELSEA']


def _asegurar_equipos_iniciales():
    existentes = {equipo.nombre: equipo for equipo in Equipo.objects.all()}

    if 'ATHETIC' in existentes and 'ATHLETIC' not in existentes:
        equipo = existentes['ATHETIC']
        equipo.nombre = 'ATHLETIC'
        equipo.save()
        existentes.pop('ATHETIC')
        existentes['ATHLETIC'] = equipo

    for nombre in EQUIPOS_BASE:
        Equipo.objects.get_or_create(nombre=nombre)


def _crear_partidos_iniciales():
    _asegurar_equipos_iniciales()
    equipos = list(Equipo.objects.order_by('nombre'))
    if len(equipos) < 2 or Partido.objects.exists():
        return

    for equipo_local, equipo_visitante in combinations(equipos, 2):
        Partido.objects.create(
            equipo_local=equipo_local,
            equipo_visitante=equipo_visitante,
        )


def _recalcular_tabla():
    for equipo in Equipo.objects.all():
        equipo.puntos = 0
        equipo.partidos_jugados = 0
        equipo.victorias = 0
        equipo.empates = 0
        equipo.derrotas = 0
        equipo.goles_a_favor = 0
        equipo.goles_en_contra = 0
        equipo.save()

    for partido in Partido.objects.filter(jugado=True).select_related('equipo_local', 'equipo_visitante'):
        local = partido.equipo_local
        visitante = partido.equipo_visitante
        goles_local = partido.goles_local or 0
        goles_visitante = partido.goles_visitante or 0

        local.partidos_jugados += 1
        visitante.partidos_jugados += 1
        local.goles_a_favor += goles_local
        local.goles_en_contra += goles_visitante
        visitante.goles_a_favor += goles_visitante
        visitante.goles_en_contra += goles_local

        if goles_local > goles_visitante:
            local.victorias += 1
            local.puntos += 3
            visitante.derrotas += 1
        elif goles_local < goles_visitante:
            visitante.victorias += 1
            visitante.puntos += 3
            local.derrotas += 1
        else:
            local.empates += 1
            visitante.empates += 1
            local.puntos += 1
            visitante.puntos += 1

        local.save()
        visitante.save()


def _obtener_contexto_dashboard(usuario):
    _crear_partidos_iniciales()
    _recalcular_tabla()

    equipos = Equipo.objects.order_by(
        '-puntos',
        '-victorias',
        '-goles_a_favor',
        'goles_en_contra',
        'nombre',
    )
    partidos = Partido.objects.select_related('equipo_local', 'equipo_visitante').order_by(
        'equipo_local__nombre',
        'equipo_visitante__nombre',
    )
    finalista = equipos.first()

    return {
        'usuario': usuario,
        'equipos': equipos,
        'partidos': partidos,
        'finalista': finalista,
    }


def login_view(request):
    if request.session.get('usuario'):
        return redirect('dashboard')

    if request.method == 'POST':
        usuario = request.POST.get('username')
        password = request.POST.get('password')

        if usuario == 'admin' and password == '1234':
            request.session['usuario'] = usuario
            return redirect('dashboard')

        return render(request, 'iniciosesion.html', {'error': 'Datos incorrectos'})

    return render(request, 'iniciosesion.html')


def inicio_view(request):
    usuario = request.session.get('usuario')
    if not usuario:
        return redirect('login')

    return render(request, 'dashboard.html', _obtener_contexto_dashboard(usuario))


def dashboard(request):
    return inicio_view(request)


def logout_view(request):
    request.session.pop('usuario', None)
    return redirect('login')


def reiniciar_torneo_view(request):
    Partido.objects.update(goles_local=None, goles_visitante=None, jugado=False)
    _recalcular_tabla()
    return redirect('dashboard')


def reiniciar_torneo(request):
    return reiniciar_torneo_view(request)


def registrar_resultado_view(request, partido_id):
    if request.method != 'POST':
        return redirect('dashboard')

    partido = get_object_or_404(Partido, id=partido_id)
    partido.goles_local = int(request.POST.get('goles_local', 0))
    partido.goles_visitante = int(request.POST.get('goles_visitante', 0))
    partido.jugado = True
    partido.save()

    _recalcular_tabla()
    return redirect('dashboard')


def registrar_resultado(request, partido_id):
    return registrar_resultado_view(request, partido_id)
