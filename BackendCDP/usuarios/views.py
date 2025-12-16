# from rest_framework import status, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from .serializers import LoginSerializer


from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import LoginSerializer

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["usuario"]
        password = serializer.validated_data["contrasena"]

        User = get_user_model()

        # Traer usuario con tipo_usuario precargado para evitar queries extra
        user = User.objects.select_related('tipo_usuario').filter(usuario=username).first()

        if not user or not user.check_password(password):
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)

        # Crear tokens JWT
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Agregar datos adicionales al token
        access["nombre"] = user.nombre
        access["tipo_usuario"] = getattr(user.tipo_usuario, "descripcion", None)

        return Response({
            "refresh": str(refresh),
            "access": str(access),
            "nombre": user.nombre,
            "tipo_usuario": access["tipo_usuario"]
        })


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Falta el refresh token"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Token inválido o ya usado"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Sesión cerrada correctamente"}, status=status.HTTP_200_OK)
