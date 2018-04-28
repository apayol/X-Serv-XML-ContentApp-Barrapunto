from django.conf.urls import patterns, include, url
from django.contrib import admin
from XMLContentAppBarrapunto import views
from django.contrib.auth.views import logout
from django.contrib.auth.views import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.inicio, name="Página inicio"),
    url(r'^logout', logout),
    url(r'^login', login),
    url(r'^accounts/profile/', views.login_exito, name="Login hecho"),
    url(r'(.+)', views.pagina, name="Página"),
)
