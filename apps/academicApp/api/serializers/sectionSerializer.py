from rest_framework import serializers
from django.contrib.auth.models import Group
from ...models import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class SectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'section_name', 'teacher_guide', 'signature']

    """ Realiza la actualización de asignación de un profesor guía a una sección """
    def update(self, instance, validated_data):
        new_teacher_guide = validated_data.get('teacher_guide', None)
        old_teacher_guide = instance.teacher_guide

        # Obtenemos si existen los grupos Profesor y Profesor Guía
        try:
            group_profesor = Group.objects.get(name="Profesor")
            group_profesor_guia = Group.objects.get(name="Profesor Guía")
        except Group.DoesNotExist:
            raise serializers.ValidationError(
                "Grupos 'Profesor' o 'Profesor Guía' no existen en el sistema."
            )

        # Se configura el profesor anterior para eliminar su rol de profesor guía si no tiene más secciones asignadas
        if old_teacher_guide and old_teacher_guide != new_teacher_guide:
            # Verifica si el profesor anterior no tiene más secciones asignadas
            if not Section.objects.filter(teacher_guide=old_teacher_guide).exclude(id=instance.id).exists():
                print(f"El profesor anterior {old_teacher_guide} no tiene más secciones. Cambiando al grupo 'Profesor'.")
                old_teacher_guide.group = group_profesor
                old_teacher_guide.save()

        # Se configura el nuevo profesor guía 
        if new_teacher_guide and new_teacher_guide.group == group_profesor:
            print(f"El nuevo profesor {new_teacher_guide} tiene el grupo 'Profesor'. Actualizando a 'Profesor Guía'.")
            new_teacher_guide.group = group_profesor_guia
            new_teacher_guide.save()

        # Actualizar los datos de la sección
        instance = super().update(instance, validated_data)
        return instance