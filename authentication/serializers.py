from rest_framework import serializers
from authentication.models import Usuario, RolUser,FacultyUser, Carrera
from conf.models import Rol

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class RolUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolUser
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'descripcion': instance.descripcion,
            'rol': instance.rol.id,
            'rol_descripcion': instance.rol.descripcion,
            'user': instance.user.username,
            'user_username': instance.user.username,
            'user_nombres': instance.user.nombres + ' ' + instance.user.apellidos
        }
    

class FacultyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyUser
        fields = '__all__'
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'descripcion': instance.descripcion,
            'carrera': instance.carrera.id,
            'carrera_descripcion': instance.carrera.descripcion,
            'user': instance.user.username,
            'user_username': instance.user.username,
            'user_nombres': instance.user.nombres + ' ' + instance.user.apellidos
        }


