from django.http import JsonResponse

from ..Parsers import Parsers
from ..models import Sintoma


class SintomaController:
    p = Parsers()

    def listar(self):
        sintomas = self.p.sintomasToDict(Sintoma.objects.all())
        return JsonResponse(sintomas, safe=False, json_dumps_params={'ensure_ascii': False})