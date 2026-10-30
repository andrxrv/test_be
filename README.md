# test_be

Pruebas de API para Restful-Booker, ejecutadas con `pytest`.

## Requisitos

- Python instalado.
- Acceso a Internet para conectarse a `https://restful-booker.herokuapp.com`.

## Instalar dependencias

Desde la carpeta del proyecto, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar las pruebas

Ejecutar todos los casos:

```powershell
python -m pytest
```

Ejecutar un archivo:

```powershell
python -m pytest .\tests\test_booking.py
```

Ejecutar un caso específico usando su nombre:

```powershell
python -m pytest .\tests\test_booking.py::test_create_booking
```

Para mostrar más detalle del resultado, agrega `-v` al comando. La configuración del proyecto ya activa esta opción por defecto.

## Configuración opcional

Por defecto, las pruebas usan `https://restful-booker.herokuapp.com` y las credenciales `admin` / `password123`. Se pueden sobrescribir con estas variables de entorno en PowerShell:

```powershell
$env:BOOKER_BASE_URL = "https://restful-booker.herokuapp.com"
$env:BOOKER_USERNAME = "admin"
$env:BOOKER_PASSWORD = "password123"
```
