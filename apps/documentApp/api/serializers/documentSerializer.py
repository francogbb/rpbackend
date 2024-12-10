from rest_framework import serializers
from ...models import Document
from apps.userApp.models import Profile, CustomGroup, GroupUser
from apps.documentApp.models import TypeDocument

class DocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Document
        fields = '__all__'
    def validate(self, data):
        # Verifica si el método es POST (creación)
        if self.instance is None and 'document' not in data:
            raise serializers.ValidationError({"document": "El campo 'document' es obligatorio al crear el documento."})
        return data

    def update(self, instance, validated_data):
        # Excluye el campo `document` de los datos validados si está presente
        validated_data.pop('document', None)
        
        # Llama al método `update` del padre con los datos restantes
        return super().update(instance, validated_data)
    
        
class DocumentSerializerPublic(serializers.ModelSerializer):
    author_names = serializers.SerializerMethodField()  # Campo calculado para nombres de autores
    teacher_guide_name = serializers.SerializerMethodField()  # Campo calculado para el nombre del profesor
    type_document_name = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'abstract',
            'type_access',
            'area',
            'academic_degree',
            'qualification',
            'publisher',
            'identifier',
            'teacher_guide',
            'teacher_guide_name',
            'entry_date',
            'available_date',
            'publication_year',
            'author_names',  # Incluye el campo calculado en los fields
            'type_document',
            'type_document_name',
        ]
    
    def get_author_names(self, obj):
        # Filtra GroupUser por el grupo del autor (verifica que `obj.author` esté correcto)
        group_users = GroupUser.objects.filter(group=obj.author)  
        
        # Extrae los nombres de los estudiantes asociados al grupo
        return [group_user.student for group_user in group_users]  # Ajusta según los campos en `GroupUser`

    def get_teacher_guide_name(self, obj):
        # Si `teacher_guide` es un ID o nombre de perfil almacenado como texto, busca el perfil correspondiente
        try:
            profile = Profile.objects.get(id=obj.teacher_guide)  # Ajusta si `teacher_guide` almacena un ID
            return f"{profile.first_name} {profile.last_name}"
        except Profile.DoesNotExist:
            return None  # Retorna None si no existe el perfil
        except ValueError:
            return obj.teacher_guide  # Si `teacher_guide` es un nombre de texto, retorna directamente el valor
    
    def get_type_document_name(self, obj):
            """
            Obtiene el nombre del tipo de documento.
            """
            try:
                type_document = TypeDocument.objects.get(id=obj.type_document_id)  # Usa `type_document_id` si es una clave foránea
                return type_document.type_name  # Ajusta según el nombre del campo en el modelo TypeDocument
            except TypeDocument.DoesNotExist:
                return None  # Si no existe el tipo de documento
            except ValueError:
                return obj.type_document  # Retorna directamente si no es válido