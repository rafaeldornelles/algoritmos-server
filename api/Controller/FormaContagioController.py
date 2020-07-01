from django.http import JsonResponse

from ..models import FormaContagio
from ..Parsers import Parsers

class FormaContagioController:
    p = Parsers()
    def listar(self):
        formasContagio = self.p.formasContagioToDict(FormaContagio.objects.all())
        return JsonResponse(formasContagio, safe=False, json_dumps_params={'ensure_ascii':False})