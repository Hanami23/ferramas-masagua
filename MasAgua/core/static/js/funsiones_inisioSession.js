function IniciarSesion() {
    // Obtener los valores de los campos de email y contraseña
    let expresionRegularEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    let username = document.getElementById('username').value;
    let contraseña = document.getElementById('contraseña').value;

    // Expresión regular para validar el formato de correo electrónico
    

    // Validar el correo electrónico
    if (nom.length <= 6) {
        alert("Correo electrónico no válido");
        document.getElementById('username').focus();
        return;
    }
    else{
        
        if (contraseña === '') {
            alert("La contraseña no puede estar vacía");
            document.getElementById('contraseña').focus();
            return;
        }
       
     else{
        alert('Bienvendo '+ email +' nuevamente');

     }  
    } 
     // Después de mostrar el mensaje, puedes redireccionar a otra página
    // Crear un enlace <a> con el atributo href que apunte a la página destino
    let enlace = document.createElement('a');
    enlace.href = 'incio.html';
    // Simular un clic en el enlace para redireccionar a la página destino
    enlace.click();
}

    function registrar() {
    let expresionRegularEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    let username = document.getElementById('username').value;
    let fono = document.getElementById('fono').value;
    let correo = document.getElementById('correo').value;
    let contra = document.getElementById('contra').value;

    // Validación del nombre
    if (username.length <= 6) {
        alert("Ingrese su nombre de usuario");
        document.getElementById('nom').focus();
        return;
    }

    // Validación del correo electrónico
    if (correo === '' || !expresionRegularEmail.test(correo)) {
        alert("Correo electrónico no válido");
        document.getElementById('correo').focus();
        return;
    }

    // Validación del número de teléfono
    if (fono.length !== 9) {
        alert("Número de teléfono no válido. Debe tener 9 dígitos");
        document.getElementById('fono').focus();
        return;
    }

    // Validación de la contraseña
    if (contra === '') {
        alert("La contraseña no puede estar vacía");
        document.getElementById('contra').focus();
        return;
    }
    // Si todas las validaciones pasan, mostrar mensaje de bienvenida y redirigir
    alert('¡Bienvenido ' + nom + '!');
     // Después de mostrar el mensaje, puedes redireccionar a otra página
    // Crear un enlace <a> con el atributo href que apunte a la página destino
    let enlace = document.createElement('a');
    enlace.href = 'incio.html';
    // Simular un clic en el enlace para redireccionar a la página destino
    enlace.click();
};