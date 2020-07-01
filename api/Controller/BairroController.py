from django.http import JsonResponse
import sys
sys.path.insert(0, '/covidometro/api/Parsers')
sys.path.insert(0, '/covidometro/api/models')
from ..Parsers import Parsers
from ..models import Caso, Bairro


class BairroController:
    p = Parsers()

    def listar(self):
        bairros = self.p.bairrosToDict(Bairro.objects.all())
        for bairro in bairros:
            bairro['casos'] = len(Caso.objects.filter(paciente__bairro__id=bairro['id']))
        return  JsonResponse(bairros, safe=False, json_dumps_params={'ensure_ascii': False})
