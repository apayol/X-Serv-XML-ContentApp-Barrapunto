from django.shortcuts import render
from .models import Pages
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


FORMULARIO_PAGE = """
    <form action="" method="POST">
        Contenido:
        <input type="text" name="page" value="">
        <input type="submit" value="Enviar">
    </form>
"""

def logg(request):
    if request.user.is_authenticated():
        logged = "> Logged in as " + request.user.username
        logged += ". <a href='/logout'> Logout </a><br><br>"
    else:
        logged = "> Not logged in. "
        logged += "<a href='/login'> Login </a><br><br>"
    return logged


def inicio(request):
    if request.method == "GET":
        titulo = "<h3>Bienvenido a XML-ContentApp-Barrapunto</h3>"
        respuesta = "<br>La lista de páginas guardadas es:<br>"
        paginas = Pages.objects.all()
        for pagina in paginas:
            respuesta += "<ul><li>" + pagina.name + " => "
            respuesta += pagina.page + "</ul></li>"
        logged = logg(request)
    else:
        respuesta = "Método no permitido"
    return HttpResponse(titulo + logged + respuesta)


@csrf_exempt
def pagina(request, name):
    logged = logg(request)

    if request.method == "GET":
        try:
            pagina = Pages.objects.get(name=name)
            respuesta = pagina.page + "<br><br>"
            if request.user.is_authenticated():
                respuesta += "¿Editar esta página?"
                respuesta += FORMULARIO_PAGE
            else:
                respuesta += "Haz log in para editar."

        except Pages.DoesNotExist:
            logged = logg(request)
            if request.user.is_authenticated():
                respuesta = "La página no existe. ¿Crear nueva entrada?"
                respuesta += "<br><br>Nombre: " + name
                respuesta += FORMULARIO_PAGE
            else:
                respuesta = "La página no existe. Haz log in para crearla"
            return HttpResponseNotFound(logged + respuesta)

    elif request.method == "POST":
        try: #  editar contenido
            busco = Pages.objects.get(name=name)
            page = request.POST["page"]
            nueva = Pages(id=busco.id, name=name, page=page)
            nueva.save(force_update=True) #  sobreescribir
        except Pages.DoesNotExist: #  crear nueva entrada
            page = request.POST["page"]
            nueva = Pages(name=name, page=page)
            nueva.save()
        respuesta = "Página actualizada con éxito"
    
    else:
        respuesta = "Método no permitido"
    return HttpResponse(logged + respuesta)

def login_exito (request):
    respuesta = "Logged in as " + request.user.username
    respuesta += " successfully"
    return HttpResponse(respuesta)
