<!-- Entorno de activación -->
..\proyecto_cdp_env\Scripts\activate

<!-- Credenciales -->
username: @dministrador_cdp
password: LaVie!sBe!!a+

<!-- Proceso para realizar cambio de contrase;a forzado -->
python manage.py shell
from django.contrib.auth.models import User

user = User.objects.get(username='tu_usuario')
user.set_password('nueva_contraseña_segura')
user.save()

<!-- APIS Usuarios -->

| Endpoint                            | Método                  | Descripción                                       |
| ----------------------------------- | ----------------------- | ------------------------------------------------- |
| `/api/usuarios/usuarios/`           | GET, POST               | Listar todos / Crear nuevo usuario                |
| `/api/usuarios/usuarios/{id}/`      | GET, PUT, PATCH, DELETE | Ver, actualizar o eliminar usuario por ID         |
| `/api/usuarios/tipo_usuarios/`      | GET, POST               | Listar todos / Crear nuevo tipo de usuario        |
| `/api/usuarios/tipo_usuarios/{id}/` | GET, PUT, PATCH, DELETE | Ver, actualizar o eliminar tipo de usuario por ID |
| `/api/usuarios/auth/`               | POST                    | Autenticación con usuario y contraseña            |

