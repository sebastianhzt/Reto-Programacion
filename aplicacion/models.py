from django.db import models


class Equipo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    puntos = models.IntegerField(default=0)
    partidos_jugados = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    empates = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    goles_a_favor = models.IntegerField(default=0)
    goles_en_contra = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    @property
    def diferencia_goles(self):
        return self.goles_a_favor - self.goles_en_contra


class Partido(models.Model):
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_local', on_delete=models.CASCADE)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitante', on_delete=models.CASCADE)
    goles_local = models.IntegerField(null=True, blank=True)
    goles_visitante = models.IntegerField(null=True, blank=True)
    jugado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"
