from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        password = request.POST.get('password')

        if usuario == 'admin' and password == '1234':
            return redirect('inicio')
        else:
            return render(request, 'iniciosesion.html', {'error': 'Datos incorrectos'})

    return render(request, 'iniciosesion.html')


def inicio_view(request):
    return render(request, 'iniciosesion.html')

