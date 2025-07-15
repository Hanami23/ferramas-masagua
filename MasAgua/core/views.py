from django.shortcuts import render, redirect ,get_object_or_404 #redireccionar
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login  #login autentifica y logea 
from django.http import JsonResponse, HttpResponse
from django.urls import reverse  #Esto se asegura de que las URLs estén bien formadas y completamente calificadas (por ejemplo: http://127.0.0.1:8000/pago-exitoso/), que es lo que MercadoPago espera.
from .models import Producto, Boleta, DetalleBoleta

from django.db.models import Sum
from django.shortcuts import render
from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone     

#mercadopago 
import mercadopago

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

def catalogo(request):
    productos = Producto.objects.all()  # ← Aquí sí traes todos los productos
    return render(request, 'catalogo.html', {'productos': productos})  # ← Y aquí los pasas al template

@login_required
def seguimiento(request):
    return render(request, 'seguimiento.html')

def iniciar_sesion(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'

    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas', 'next': next_url})

    return render(request, 'login.html', {'next': next_url})

def user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        fono = request.POST['fono']  # Este aún no se guarda, pero lo puedes mostrar o usar después
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'login.html', {'error': 'Las contraseñas no coinciden'})

        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': 'El nombre de usuario ya existe'})

        if User.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'El correo ya está registrado'})

        # 🔥 ESTA ES LA LÍNEA QUE GUARDA EN LA BASE DE DATOS LOCAL
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        return redirect('login')  # redirige a login luego del registro

    return redirect('login')

#todo del carrito
@require_POST
@login_required
@require_POST
@login_required
def modificar_cantidad(request):
    producto_id = request.POST.get('producto_id')
    accion = request.POST.get('accion')

    carrito = request.session.get('carrito', {})  # carrito = { "1": 2, "2": 1 }

    if producto_id in carrito:
        cantidad_actual = carrito[producto_id]

        if accion == 'sumar':
            cantidad_nueva = cantidad_actual + 1
        elif accion == 'restar' and cantidad_actual > 1:
            cantidad_nueva = cantidad_actual - 1
        else:
            return JsonResponse({'success': False, 'error': 'Cantidad inválida'})

        carrito[producto_id] = cantidad_nueva
        request.session['carrito'] = carrito

        try:
            producto = Producto.objects.get(pk=int(producto_id))
            nuevo_subtotal = cantidad_nueva * producto.precio
        except Producto.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Producto no encontrado en la base de datos'})

        # 🔸 Calcular el nuevo total general del carrito
        total = 0
        for pid, cantidad in carrito.items():
            try:
                prod = Producto.objects.get(pk=int(pid))
                total += prod.precio * cantidad
            except Producto.DoesNotExist:
                continue

        return JsonResponse({
            'success': True,
            'nueva_cantidad': cantidad_nueva,
            'nuevo_subtotal': nuevo_subtotal,
            'nuevo_total': total
        })

    return JsonResponse({'success': False, 'error': 'Producto no encontrado en el carrito'})


def carrito(request):
    return render(request, 'carrito.html')

def ver_carrito(request):
    # Paso 1: Obtener el carrito desde la sesión
    carrito = request.session.get('carrito', {})  # Diccionario {id: cantidad}

    productos_carrito = []
    total = 0

    # Paso 2: Recorrer el carrito
    for producto_id_str, cantidad in carrito.items():
        try:
            producto_id = int(producto_id_str)  # clave puede venir como string
            producto = Producto.objects.get(pk=producto_id)
            subtotal = producto.precio * cantidad
            productos_carrito.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Producto.DoesNotExist:
            continue

    # Paso 3: Enviar al template
    return render(request, 'carrito.html', {
        'productos': productos_carrito,
        'total': total
    })

@require_POST
def agregar_al_carrito(request):
    try:
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 1))

        if not producto_id:
            return JsonResponse({'error': 'ID de producto no enviado'}, status=400)

        carrito = request.session.get('carrito', {})

        if producto_id in carrito:
            carrito[producto_id] += cantidad
        else:
            carrito[producto_id] = cantidad

        request.session['carrito'] = carrito

        return JsonResponse({'success': True, 'mensaje': 'Producto agregado al carrito'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@require_POST
def eliminar_del_carrito(request):
    producto_id = request.POST.get('producto_id')
    carrito = request.session.get('carrito', {})

    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito

    return redirect('carrito')

def calcular_totales(carrito):
    total = 0
    productos = []

    for producto_id_str, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(pk=int(producto_id_str))
            subtotal = producto.precio * cantidad
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal,
            })
            total += subtotal
        except Producto.DoesNotExist:
            continue

    return productos, total


#pago mercadopago
sdk = mercadopago.SDK("TEST-5620329214983463-070223-a0dfe89354f273abf1a18098ef40fa21-1262225673")  # Reemplaza por tu token real

@login_required
def pagar(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('carrito')

    productos = []
    total = 0

    for pid, cantidad in carrito.items():
        producto = Producto.objects.get(id=pid)
        productos.append({
            "title": producto.nombre,
            "quantity": cantidad,
            "unit_price": float(producto.precio)
        })
        total += producto.precio * cantidad

    # Construcción segura de URLs completas para back_urls
    success_url = "https://welcome-grubworm-closely.ngrok-free.app/pago-exitoso/"
    failure_url = "https://welcome-grubworm-closely.ngrok-free.app/pago-fallido/"

    # Diagnóstico: imprime las URLs generadas
    print("🔗 URL ÉXITO:", success_url)                 
    print("🔗 URL FALLO:", failure_url)

    preference_data = {
        "items": productos,
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": success_url  # ✅ requerido para evitar el error mercado pago
        },
        "auto_return": "approved",
    }

    try:
        preference = sdk.preference().create(preference_data)
        print("🌐 RESPUESTA DE MERCADOPAGO:", preference)
    except Exception as e:
        print("❌ Error creando preferencia:", str(e))
        return render(request, "carrito.html", {
            "error": "Error al generar preferencia con MercadoPago.",
            "detalle": str(e),
        })

    # Validar respuesta
    if "response" in preference and "init_point" in preference["response"]:
        print("🔗 INIT_POINT:", preference["response"]["init_point"])
        return redirect(preference["response"]["init_point"])
    else:
        print("❌ No se encontró init_point. Preferencia:", preference)  # <-- MUY IMPORTANTE
        return render(request, "carrito.html", {
            "error": "Error al generar el pago con MercadoPago. Verifica los datos o la clave secreta.",
            "debug": preference
        })
        

@login_required
def pago_exitoso(request):
    payment_id = request.GET.get('payment_id')
    if not payment_id:
        return redirect('carrito')

    # Verificar el estado del pago
    try:
        payment = sdk.payment().get(payment_id)
        status = payment["response"]["status"]
        print("✅ Estado del pago:", status)
        if status != "approved":
            return redirect('pago_fallido')
    except Exception as e:
        print("❌ Error verificando pago:", e)
        return redirect('pago_fallido')

    carrito = request.session.get('carrito', {})
    if not carrito:
        print("⚠️ Carrito vacío al momento de crear boleta")
        return redirect('carrito')

    print("📦 Carrito recibido:", carrito)

    boleta = Boleta.objects.create(usuario=request.user, total=0)
    total = 0

    for pid_str, cantidad in carrito.items():
        try:
            pid = int(pid_str)
            producto = Producto.objects.get(id=pid)
            subtotal = producto.precio * cantidad

            # Log para depurar
            print(f"➡️ Añadiendo producto a boleta: {producto.nombre}, cantidad: {cantidad}")

            DetalleBoleta.objects.create(
                boleta=boleta,
                producto=producto,
                descripcionCompra=producto.nombre,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

            producto.stock -= cantidad
            producto.save()

            total += subtotal
        except Producto.DoesNotExist:
            print(f"❌ Producto con ID {pid} no encontrado")

    boleta.total = total
    boleta.save()

    # Limpiar carrito
    request.session['carrito'] = {}

    return render(request, 'pago_exitoso.html', {'boleta': boleta})

def pago_fallido(request):
    return render(request, 'pago_fallido.html')


def Pedidos_Activos(request):
    hoy = timezone.now().date()
    labels = []
    data = []

    for i in range(4, -1, -1):  # 4 días atrás hasta hoy
        dia = hoy - timedelta(days=i)
        total_dia = Boleta.objects.filter(fecha__date=dia).aggregate(total=Sum('total'))['total'] or 0
        labels.append(dia.strftime('%Y-%m-%d'))
        data.append(total_dia)

    total_general = Boleta.objects.aggregate(Sum('total'))['total__sum'] or 0

    boletas = Boleta.objects.filter(usuario=request.user).order_by('-fecha')

    # 🔸 Vincular los detalles a cada boleta
    boletas_con_detalles = []
    for boleta in boletas:
        detalles = DetalleBoleta.objects.filter(boleta=boleta)
        boletas_con_detalles.append({
            'boleta': boleta,
            'detalles': detalles
        })

    context = {
        'labels': labels,
        'data': data,
        'total_general': total_general,
        'boletas_con_detalles': boletas_con_detalles,
    }
    return render(request, 'Pedidos_Activos.html', context)


#parte del transportista
def es_transportista(user):
    return user.is_superuser or user.groups.filter(name='transportista').exists()


@user_passes_test(es_transportista, login_url='/no-autorizado/')
@login_required
def panel_transportista(request):
    print(f"➡️ Usuario autenticado: {request.user.username}")
    print(f"➡️ ¿Es transportista? {es_transportista(request.user)}")
     # Obtén todas las boletas (o filtra según lo necesario)
    boletas = Boleta.objects.all()

    return render(request, 'panel_transportista.html', {
        'boletas': boletas
    })

@login_required
@user_passes_test(es_transportista)
def marcar_entregado(request, boleta_id):
    boleta = get_object_or_404(Boleta, id=boleta_id)
    if boleta.estado_entrega == 'en_camino':
        boleta.estado_entrega = 'entregado'
        boleta.save()
    return redirect('panel_transportista')

def no_autorizado(request):
    return HttpResponse("No estás autorizado para ver esta página.", status=403)