document.querySelectorAll('.agregar-carrito').forEach(boton => {
  boton.addEventListener('click', function () {
    const productoId = this.dataset.productoId;
    console.log("Click en producto", productoId); // Prueba

    fetch('/agregar-al-carrito/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': obtenerCSRFToken(),
      },
      body: new URLSearchParams({
        producto_id: productoId,
        cantidad: 1,
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log("📦 Respuesta:", data);
      if (data.success) {
        const modal = new bootstrap.Modal(document.getElementById('modalCarrito'));
        modal.show();
      } else {
        alert('Error: ' + data.error);
      }
    })
    .catch(error => {
      console.error('Error en fetch:', error);
      alert('Error al agregar al carrito');
    });
  });
});

function obtenerCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
