from rest_framework import serializers
from .models import Usuario

class LoginSerializer(serializers.Serializer):
    usuario = serializers.CharField()
    contrasena = serializers.CharField(write_only=True)
