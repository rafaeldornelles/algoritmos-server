import json

from django.http import JsonResponse

from ..models import Paciente, Bairro, Locais
from ..Parsers import Parsers


class PacienteController:
    p = Parsers()

    def listar(self):
        pacientes = self.p.pacientesToDict(Paciente.objects.all())
        return JsonResponse(pacientes, safe=False, json_dumps_params={'ensure_ascii': False})

    def cadastrar(self, request):
        data = json.loads(request.body)
        bairro = Bairro.objects.get(id=data['bairro']['id'])
        locaisIds = [local['id'] for local in data['locaisVisitados']]
        paciente = Paciente(nome=data["nome"], bairro=bairro)
        paciente.save()
        paciente.locaisVisitados.set([Locais.objects.get(id=id) for id in locaisIds])
        paciente.save()
        return JsonResponse(self.p.pacienteToDict(paciente))

    def getById(self, id):
        paciente = self.p.pacienteToDict(Paciente.objects.get(id=id))
        return JsonResponse(paciente, json_dumps_params={'ensure_ascii': False})

    def atualizar(self, request, id):
        data = json.loads(request.body)
        paciente = Paciente.objects.get(id=id)
        paciente.nome = data['nome']
        paciente.bairro = Bairro.objects.get(id=data['bairro']['id'])
        locaisIds = [local['id'] for local in data['locaisVisitados']]
        paciente.locaisVisitados.set([Locais.objects.get(id=id) for id in locaisIds])
        paciente.save()
        return JsonResponse(self.p.pacienteToDict(paciente))

    def deletar(self, id):
        paciente = Paciente.objects.get(id=id)
        paciente_dict = self.p.pacienteToDict(paciente)
        paciente.delete()
        return JsonResponse(paciente_dict)