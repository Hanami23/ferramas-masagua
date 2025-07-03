document.querySelectorAll('.modificar-cantidad').forEach(boton => {
    boton.addEventListener('click', function () {
        const productoId = this.dataset.productoId;
        const accion = this.dataset.accion;

        fetch('/modificar-cantidad/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': obtenerCSRFToken(),
          },
          body: new URLSearchParams({
            producto_id: productoId,
            accion: accion,
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            document.getElementById(`cantidad-${productoId}`).textContent = data.nueva_cantidad;
            document.getElementById(`subtotal-${productoId}`).textContent = data.nuevo_subtotal;
            // También podrías actualizar el total general si lo devuelves desde la vista
          } else {
            alert('⚠️ ' + data.error);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Error al modificar la cantidad.');
        });
      });
    });

function obtenerCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
