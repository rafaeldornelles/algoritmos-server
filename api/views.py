from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Bairro, Caso, Locais, Paciente, Sintoma, FormaContagio
from .Parsers import Parsers
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
p = Parsers()
def bairros(request):
    bairros = p.bairrosToDict(Bairro.objects.all())
    for bairro in bairros:
        bairro['casos'] = len(Caso.objects.filter(paciente__bairro__id=bairro['id']))

    return  JsonResponse(bairros, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def locais(request):
    if request.method == "GET":
        locais = p.locaisToDict(Locais.objects.all())
        for local in locais:
            local['casos'] = len(Caso.objects.filter(paciente__locaisVisitados__id = local['id']))
        return JsonResponse(locais, safe=False, json_dumps_params={'ensure_ascii': False})

    elif request.method == "POST":
        #try:
        body = json.loads(request.body)
        local = Locais(nome=body["nome"], endereco=body["endereco"])
        local.save()
        return JsonResponse(p.localToDict(local), json_dumps_params={'ensure_ascii': False})
        #except:
            #return HttpResponse("deu ruim")

@csrf_exempt
def pacientes(request):
    if request.method == "GET":
        pacientes = p.pacientesToDict(Paciente.objects.all())
        return JsonResponse(pacientes, safe=False, json_dumps_params={'ensure_ascii': False})

    elif request.method == "POST":
        data = json.loads(request.body)
        bairro = Bairro.objects.get(id=data['bairro']['id'])
        locaisIds = [local['id'] for local in data['locaisVisitados']]
        paciente = Paciente(nome=data["nome"], bairro=bairro)
        paciente.save()
        paciente.locaisVisitados.set([Locais.objects.get(id=id) for id in locaisIds])
        paciente.save()
        return JsonResponse(p.pacienteToDict(paciente))

@csrf_exempt
def paciente(request, paciente_id):
    if request.method == "GET":
        paciente = p.pacienteToDict(Paciente.objects.get(id=paciente_id))
        return JsonResponse(paciente, json_dumps_params={'ensure_ascii': False})

    elif request.method == "PUT":
        data = json.loads(request.body)
        paciente = Paciente.objects.get(id=paciente_id)
        paciente.nome = data['nome']
        paciente.bairro = Bairro.objects.get(id=data['bairro']['id'])
        locaisIds = [local['id'] for local in data['locaisVisitados']]
        paciente.locaisVisitados.set([Locais.objects.get(id=id) for id in locaisIds])
        paciente.save()
        return JsonResponse(p.pacienteToDict(paciente))

    elif request.method == "DELETE":
        paciente = Paciente.objects.get(id=paciente_id)
        paciente_dict = p.pacienteToDict(paciente)
        paciente.delete()
        return JsonResponse(paciente_dict)

def sintomas(request):
    if request.method == "GET":
        sintomas = p.sintomasToDict(Sintoma.objects.all())
        return JsonResponse(sintomas, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def casos(request):
    if request.method == "GET":
        casos = Caso.objects.all()
        casos_dict = p.casosToDict(casos)
        return JsonResponse(casos_dict, safe=False, json_dumps_params={'ensure_ascii':False})
    elif request.method == "POST":
        data = json.loads(request.body)
        paciente = Paciente.objects.get(id=data['paciente']['id'])
        formaContagio = FormaContagio.objects.get(id=data['formaContagio']['id'])
        dataInicioSintomas = datetime.strptime(data['dataInicioSintomas'], '%Y-%m-%d')
        dataRelato = datetime.now()
        caso = Caso(paciente=paciente, formaContagio=formaContagio, dataInicioSintomas=dataInicioSintomas, dataRelato=dataRelato)
        caso.save()
        caso.sintomas.set([Sintoma.objects.get(id=sintoma['id']) for sintoma in data['sintomas']])
        return JsonResponse(p.casoToDict(caso))

@csrf_exempt
def caso(request, caso_id):
    if request.method == "GET":
        caso = p.casoToDict(Caso.objects.get(id=caso_id))
        return JsonResponse(caso, json_dumps_params={'ensure_ascii': False})
    elif request.method == "PUT":
        data = json.loads(request.body)
        caso = Caso.objects.get(id=caso_id)
        caso.paciente = Paciente.objects.get(id=data['paciente']['id'])
        caso.formaContagio = FormaContagio.objects.get(id=data['formaContagio']['id'])
        caso.dataInicioSintomas = datetime.strptime(data['dataInicioSintomas'], '%Y-%m-%d')
        try:
            caso.dataFimSintomas = datetime.strptime(data['dataFimSintomas'], '%Y-%m-%d')
        except:
            pass
        caso.sintomas.set([Sintoma.objects.get(id=id) for id in data['sintomas']])
        caso.save()
        return JsonResponse(p.casoToDict(caso))
    elif request.method == "DELETE":
        caso = Caso.objects.get(id=caso_id)
        caso_dict = p.casoToDict(caso)
        caso.delete()
        return JsonResponse(caso_dict)

def casosPorBairro(request, bairro_id):
    casos = p.casosToDict(Caso.objects.filter(paciente__bairro__id = bairro_id))
    return JsonResponse(casos, safe=False, json_dumps_params={'ensure_ascii':False})

def casosPorLocalVisitado(request, local_id):
    locais = p.casosToDict(Caso.objects.filter(paciente__locaisVisitados__id = local_id))
    return JsonResponse(locais, safe=False, json_dumps_params={'ensure_ascii':False})

def formasContagio(request):
    formasContagio = p.formasContagioToDict(FormaContagio.objects.all())
    return JsonResponse(formasContagio, safe=False, json_dumps_params={'ensure_ascii':False})
