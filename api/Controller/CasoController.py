from django.http import JsonResponse

from ..Parsers import Parsers
from ..models import Caso, Paciente, FormaContagio, Sintoma
from datetime import datetime
import json

class CasoController:
    p = Parsers()
    def listar(self):
        casos = Caso.objects.all()
        casos_dict = self.p.casosToDict(casos)
        return JsonResponse(casos_dict, safe=False, json_dumps_params={'ensure_ascii': False})

    def cadastrar(self, request):
        data = json.loads(request.body)
        paciente = Paciente.objects.get(id=data['paciente']['id'])
        formaContagio = FormaContagio.objects.get(id=data['formaContagio']['id'])
        dataInicioSintomas = datetime.strptime(data['dataInicioSintomas'], '%Y-%m-%d')
        dataRelato = datetime.now()
        caso = Caso(paciente=paciente, formaContagio=formaContagio, dataInicioSintomas=dataInicioSintomas,
                    dataRelato=dataRelato)
        caso.save()
        caso.sintomas.set([Sintoma.objects.get(id=sintoma['id']) for sintoma in data['sintomas']])
        return JsonResponse(self.p.casoToDict(caso))

    def listarPorId(self, id):
        caso = self.p.casoToDict(Caso.objects.get(id=id))
        return JsonResponse(caso, json_dumps_params={'ensure_ascii': False})

    def atualizar(self, request, id):
        data = json.loads(request.body)
        caso = Caso.objects.get(id=id)
        caso.paciente = Paciente.objects.get(id=data['paciente']['id'])
        caso.formaContagio = FormaContagio.objects.get(id=data['formaContagio']['id'])
        caso.dataInicioSintomas = datetime.strptime(data['dataInicioSintomas'], '%Y-%m-%d')
        try:
            caso.dataFimSintomas = datetime.strptime(data['dataFimSintomas'], '%Y-%m-%d')
        except:
            pass
        caso.sintomas.set([Sintoma.objects.get(id=id) for id in data['sintomas']])
        caso.save()
        return JsonResponse(self.p.casoToDict(caso))

    def deletar(self, id):
        caso = Caso.objects.get(id=id)
        caso_dict = self.p.casoToDict(caso)
        caso.delete()
        return JsonResponse(caso_dict)


    def listarPorBairro(self, bairro_id):
        casos = self.p.casosToDict(Caso.objects.filter(paciente__bairro__id=bairro_id))
        return JsonResponse(casos, safe=False, json_dumps_params={'ensure_ascii': False})

    def listarPorLocal(self, local_id):
        locais = self.p.casosToDict(Caso.objects.filter(paciente__locaisVisitados__id=local_id))
        return JsonResponse(locais, safe=False, json_dumps_params={'ensure_ascii': False})