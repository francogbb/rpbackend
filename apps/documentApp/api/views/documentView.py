from rest_framework import viewsets
from rest_framework.decorators import action
from ...models import Document,Statistics
from ..serializers.documentSerializer import DocumentSerializer
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse, HttpResponseServerError
from cryptography.fernet import Fernet, InvalidToken
from rest_framework.parsers import MultiPartParser, FormParser


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permmission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser) # - Permite manejar archivos en la petición de manera mas segura
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