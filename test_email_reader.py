from unittest.mock import MagicMock
import re
from email_reader import connect_gmail, read_last_mail

# Mock de connect_gmail
def mock_connect_gmail(user, password):
    print(f"Simulando conexión con el servidor IMAP para el usuario: {user}")
    connection = MagicMock()
    connection.select.return_value = ("OK", [])
    return connection

# Mock de read_last_mail con contenido realista
def mock_read_last_mail(connection):
    print("Simulando lectura del último correo no leído...")
    # Simulamos un correo con asunto y cuerpo específicos
    return {
        "subject": "Reserva realizada",
        "body": """
        Nombre: Jesús
        Apellidos: Ropero López
        Vehículo: Dacia
        Modelo: Sandero Stepway
        Fecha de ingreso: 2025-01-08
        Fecha de salida: 2025-01-12
        """
    }

# Función para analizar el cuerpo del correo
def parse_email_body(body):
    patrones = {
        "nombre": r"Nombre:\s*(.+)",
        "apellidos": r"Apellidos:\s*(.+)",
        "vehiculo": r"Vehículo:\s*(.+)",
        "modelo": r"Modelo:\s*(.+)",
        "fecha_ingreso": r"Fecha de ingreso:\s*(\d{4}-\d{2}-\d{2})",
        "fecha_salida": r"Fecha de salida:\s*(\d{4}-\d{2}-\d{2})",
    }
    datos = {}
    for campo, patron in patrones.items():
        match = re.search(patron, body)
        if match:
            datos[campo] = match.group(1)
    return datos

# Prueba funcional con mocks
def test_with_mock():
    USER = "correo_fake@dominio.com"
    PASSWORD = "contraseña_fake"

    # Usar las funciones mockeadas
    connection = mock_connect_gmail(USER, PASSWORD)
    result = mock_read_last_mail(connection)

    # Verificar y mostrar el resultado
    if result:
        print(f"Asunto: {result['subject']}")
        print(f"Cuerpo: {result['body']}")

        # Procesar el cuerpo del correo
        parsed_data = parse_email_body(result['body'])
        print("Datos extraídos del correo:")
        for key, value in parsed_data.items():
            print(f"{key.capitalize()}: {value}")
    else:
        print("No hay correos nuevos.")

# Ejecutar la prueba
if __name__ == "__main__":
    test_with_mock()
