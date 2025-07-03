from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.iniciar_sesion, name='login'),
    path('home', views.home, name='home'),
    path('catalogo', views.catalogo, name='catalogo' ),
    path('seguimiento', views.seguimiento, name='seguimiento'),

    path('registro/', views.user_view, name='user_view'),
    path('login/', views.iniciar_sesion, name='login'),  #vista de login

    path('carrito', views.ver_carrito, name='carrito'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('modificar-cantidad/', views.modificar_cantidad, name='modificar_cantidad'),
    path('pagar/', views.pagar, name='pagar'),
    
     path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)