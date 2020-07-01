import json

from django.http import JsonResponse

from ..Parsers import Parsers
from ..models import Locais, Caso


class LocalController:
    p = Parsers()

    def listar(self):
        locais = self.p.locaisToDict(Locais.objects.all())
        for local in locais:
            local['casos'] = len(Caso.objects.filter(paciente__locaisVisitados__id=local['id']))
        return JsonResponse(locais, safe=False, json_dumps_params={'ensure_ascii': False})

    def cadastrar(self, request):
        body = json.loads(request.body)
        local = Locais(nome=body["nome"], endereco=body["endereco"])
        local.save()
        return JsonResponse(self.p.localToDict(local), json_dumps_params={'ensure_ascii': False})