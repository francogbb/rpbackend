from rest_framework import viewsets
from ...models import Document
from ..serializers.documentSerializer import DocumentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse, HttpResponseServerError
from cryptography.fernet import Fernet, InvalidToken
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permmission_classes = [AllowAny]

    @parser_classes([MultiPartParser])
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
            response['Content-Disposition'] = f'inline; filename="{documento.document.name}"'
            response.write(contenido_desencriptado) 
            
            
            return response
        except Document.DoesNotExist:
            return HttpResponse("Documento no encontrado", status=404) 
        except InvalidToken:
            return HttpResponse("Error en la desencriptación. Verifique la clave.", status=400)
        except Exception as e:
            return HttpResponseServerError(f"Error al desencriptar el documento: {str(e)}")