from rest_framework import serializers
from ...models import Document
from apps.userApp.models import Profile, CustomGroup, GroupUser
from apps.documentApp.models import TypeDocument

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    """ Verifica si el método es POST (creación) """
    def validate(self, data):
        if self.instance is None and 'document' not in data:
            raise serializers.ValidationError({"document": "El campo 'document' es obligatorio al crear el documento."})
        return data

    def update(self, instance, validated_data):
        validated_data.pop('document', None)

        return super().update(instance, validated_data)
    
        
class DocumentSerializerPublic(serializers.ModelSerializer):
    author_names = serializers.SerializerMethodField()  
    teacher_guide_name = serializers.SerializerMethodField()  
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
            'author_names',
            'type_document',
            'type_document_name',
            'teacher_name',
        ]
    
    """ Entrega los nombres de los autores """
    def get_author_names(self, obj):
        group_users = GroupUser.objects.filter(group=obj.author)  
        
        return [group_user.student for group_user in group_users]  

    """ Entrega el nombre del profesor guía """
    def get_teacher_guide_name(self, obj):
        try:
            profile = Profile.objects.get(id=obj.teacher_guide)  
            return f"{profile.first_name} {profile.last_name}"
        except Profile.DoesNotExist:
            return None  
        except ValueError:
            return obj.teacher_guide  
    
    """ Entrega el nombre del tipo de documento """
    def get_type_document_name(self, obj): 
            
            try:
                type_document = TypeDocument.objects.get(id=obj.type_document_id)  
                return type_document.type_name  
            except TypeDocument.DoesNotExist:
                return None  
            except ValueError:
                return obj.type_document  