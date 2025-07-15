from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.iniciar_sesion, name='login'),
    path('home', views.home, name='home'),
    path('catalogo', views.catalogo, name='catalogo' ),
    path('seguimiento', views.seguimiento, name='seguimiento'),

    path('registro/', views.user_view, name='user_view'),
    path('login/', views.iniciar_sesion, name='login'),  #vista de login
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('carrito', views.ver_carrito, name='carrito'),
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('modificar-cantidad/', views.modificar_cantidad, name='modificar_cantidad'),
    path('pagar/', views.pagar, name='pagar'),
    
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),

    path('Pedidos_Activos/',views.Pedidos_Activos, name='Pedidos_Activos'),

    path('panel_transportista/',views.panel_transportista, name='panel_transportista'),
    path('marcar-entregado/<int:boleta_id>/', views.marcar_entregado, name='marcar_entregado'),

    path('no-autorizado/', views.no_autorizado, name='no_autorizado'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)