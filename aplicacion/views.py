from django.shortcuts import render, redirect



def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        password = request.POST.get('password')

        if usuario == 'admin' and password == '1234':
            return redirect('inicio')  
        else:
            return render(request, 'index.html', {'error': 'Datos incorrectos'})

    return render(request, 'index.html')
# Create your views here.
