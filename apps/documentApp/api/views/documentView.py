from rest_framework import viewsets
from rest_framework.decorators import action
from ...models import Document,Statistics
from ..serializers.documentSerializer import DocumentSerializer, DocumentSerializerPublic
from ..serializers.publishFormSerializer import PublishFormAcceptSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse, HttpResponseServerError
from cryptography.fernet import Fernet, InvalidToken
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework import status
from ...models import PublishForm
from rest_framework.views import APIView


""" Actualiza campos y desencripta el documento para su visualización"""
class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser) 
    
    """ Desencripta el documento y actualiza las estadísticas """
    @action(detail=True, methods=['get'])
    def desencriptar_documento(self, request, pk=None):
        try:
            documento = Document.objects.get(pk=pk)

            if not documento.document:
                return HttpResponse("Archivo no encontrado", status=404)

            clave_encriptacion = documento.encryption_key

            if isinstance(clave_encriptacion, str):
                clave_encriptacion = clave_encriptacion.encode()  

            cipher_suite = Fernet(clave_encriptacion)

            with documento.document.open('rb') as f:
                contenido_encriptado = f.read()
                contenido_desencriptado = cipher_suite.decrypt(contenido_encriptado)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{documento.title}"'
            response.write(contenido_desencriptado)

           # Obtiene el modelo de statics de views y despues crea la estadistica 
            stats, created = Statistics.objects.get_or_create(document=documento)
            
            # Ve el tiempo real o la ultima vez que se vio el documento y si es mayor a 5 seg se suma una vista
            if not stats.last_viewed or timezone.now() - stats.last_viewed > timedelta(seconds=5):
                stats.views += 1
                stats.last_viewed = timezone.now()
                stats.save(update_fields=['views', 'last_viewed'])
            return response
        except Document.DoesNotExist:
            return HttpResponse("Documento no encontrado", status=404) 
        except InvalidToken:
            return HttpResponse("Error en la desencriptación. Verifique la clave.", status=400)
        except Exception as e:
            return HttpResponseServerError(f"Error al desencriptar el documento: {str(e)}")
    
    """ Sobrescribir el método create para manejar el guardado y cifrado del documento """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guarda la instancia temporalmente para obtener el objeto
        document_instance = serializer.save()

        if document_instance.document:
            # Obtener el nombre original del archivo del request
            original_file_name = request.FILES['document'].name

            # Genera la clave de cifrado si no existe
            if not document_instance.encryption_key:
                document_instance.encryption_key = Fernet.generate_key()
            cipher = Fernet(document_instance.encryption_key)

            # Lee el contenido del archivo
            with document_instance.document.open('rb') as file:
                pdf_content = file.read()

            # Cifrar el contenido
            encrypted_content = cipher.encrypt(pdf_content)

            # Eliminar el archivo original antes de guardar el encriptado
            document_instance.document.delete(save=False)

            # Guardar el archivo cifrado usando el nombre original
            encrypted_file_name = f'encrypted_{original_file_name}'
            document_instance.document.save(encrypted_file_name, ContentFile(encrypted_content), save=False)

            # Guardar nuevamente la instancia con el archivo cifrado
            document_instance.save()

        # Devolver la respuesta de creación
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """ Actualiza los campos excluyendo a document """
    def update(self, request, *args, **kwargs):
        # Si el campo `document` no está en el request, se elimina de los datos validados
        if 'document' not in request.data:
            partial_data = request.data.copy()
            partial_data.pop('document', None)
            serializer = self.get_serializer(self.get_object(), data=partial_data, partial=True)
        else:
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """ Actualiza solo el campo identifier """
    @action(detail=True, methods=['patch'])
    def update_identifier(self, request, pk=None):
        document_instance = self.get_object()
        identifier = request.data.get('identifier')
        
        if not identifier:
            return Response({"error": "El campo 'identifier' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        document_instance.identifier = identifier
        document_instance.save(update_fields=['identifier'])
        
        return Response({"message": "Identificador actualizado correctamente."}, status=status.HTTP_200_OK)

    """ Actualiza solo el campo type_acccess """
    @action(detail=True, methods=['patch'])
    def update_type_access(self, request, pk=None):
        document_instance = self.get_object()
        type_access = request.data.get('type_access')

        if type_access in ['true', 'false']:
            type_access = type_access == 'true'
        else:
            return Response(
                {"error": "El campo 'type_access' debe ser 'true' o 'false'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        document_instance.type_access = type_access
        document_instance.save(update_fields=['type_access'])

        return Response(
            {"message": "Acceso actualizado correctamente."},
            status=status.HTTP_200_OK
        )
        
""" Obtener campos de los documentos """
class DocumentPublicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializerPublic
    permission_classes = [AllowAny]

""" Otiene los documentos con solicitud de publicación aprobada """
class DocumentAccept(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # Obtiene los IDs de los documentos aprobados
        document_ids = PublishForm.objects.filter(state=2).values_list('document', flat=True)

        # Obtiene la data completa de los documentos según los ids obtenidos
        documents = Document.objects.filter(id__in=document_ids)
        serializer = DocumentSerializerPublic(documents, many=True)
        return Response(serializer.data)