from django.shortcuts import render
from .models import Pages
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

# Create your views here.


FORMULARIO_PAGE = """
    <form action="" method="POST">
        Contenido:
        <input type="text" name="page" value="">
        <input type="submit" value="Enviar">
    </form>
"""

barrapunto_rss = " "

class myContentHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        global barrapunto_rss
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = self.theContent
                barrapunto_rss += "<ul><li>" + self.title + "<br/>"
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.link = " Link: " + self.theContent + "."
                barrapunto_rss += "<a href=" + self.theContent + ">"
                barrapunto_rss += self.theContent + "</a></ul></li>"
                self.inContent = False
                self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

def barrapunto(request):  # extraigo noticias de barrapunto
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    url = "http://barrapunto.com/index.rss"
    rss = urllib.request.urlopen(url)
    theParser.parse(rss)
    return None

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
        respuesta = "<br>La lista de páginas guardadas es:</br>"
        paginas = Pages.objects.all()
        for pagina in paginas:
            respuesta += "<ul><li>" + pagina.name + " => "
            respuesta += pagina.page + "</ul></li>"
        logged = logg(request)
        respuesta += "<br>La lista de noticias de barrapunto es:</br>"
        barrapunto(request) # muestro últimas noticias
    else:
        respuesta = "Método no permitido"
    return HttpResponse(titulo + logged + respuesta + barrapunto_rss)


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
            respuesta += "<br>La lista de noticias de barrapunto es:</br>"
            barrapunto(request) # muestro últimas noticias
        except Pages.DoesNotExist:
            logged = logg(request)
            if request.user.is_authenticated():
                respuesta = "La página no existe. ¿Crear nueva entrada?"
                respuesta += "<br><br>Nombre: " + name
                respuesta += FORMULARIO_PAGE
                respuesta += "<br>La lista de noticias de barrapunto es:</br>"
                barrapunto(request) # muestro últimas noticias
            else:
                respuesta = "La página no existe. Haz log in para crearla"
            return HttpResponseNotFound(logged + respuesta + barrapunto_rss)

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
    
    return HttpResponse(logged + respuesta + barrapunto_rss)

def login_exito (request):
    respuesta = "Logged in as " + request.user.username
    respuesta += " successfully"
    return HttpResponse(respuesta)
