from django.views.decorators.csrf import csrf_exempt

import sys
sys.path.insert(0, '/covidometro/covidometro/api')
from .Controller.BairroController import BairroController
from .Controller.LocalController import LocalController
from .Controller.PacienteController import PacienteController
from .Controller.SintomaController import SintomaController
from .Controller.CasoController import CasoController
from .Controller.FormaContagioController import FormaContagioController


# Create your views here.
bairroController = BairroController()
localController = LocalController()
pacienteController = PacienteController()
sintomaController = SintomaController()
casoController = CasoController()
formaContagioController = FormaContagioController()

def bairros(request):
    if request.method == 'GET':
        return bairroController.listar()

@csrf_exempt
def locais(request):
    if request.method == "GET":
        return localController.listar()

    elif request.method == "POST":
        return localController.cadastrar(request)


@csrf_exempt
def pacientes(request):
    if request.method == "GET":
        return pacienteController.listar()

    elif request.method == "POST":
        return pacienteController.cadastrar(request)


@csrf_exempt
def paciente(request, paciente_id):
    if request.method == "GET":
        return pacienteController.listar()

    elif request.method == "PUT":
        return pacienteController.atualizar(request, paciente_id)

    elif request.method == "DELETE":
        return pacienteController.atualizar(request, id)

def sintomas(request):
    if request.method == "GET":
        return sintomaController.listar()

@csrf_exempt
def casos(request):
    if request.method == "GET":
        return casoController.listar()

    elif request.method == "POST":
       return casoController.cadastrar(request)

@csrf_exempt
def caso(request, caso_id):
    if request.method == "GET":
        return casoController.listarPorId(caso_id)

    elif request.method == "PUT":
        return casoController.atualizar(request, caso_id)

    elif request.method == "DELETE":
        return casoController.deletar(caso_id)

def casosPorBairro(request, bairro_id):
    if request.method == "GET":
        return casoController.listarPorBairro(bairro_id)

def casosPorLocalVisitado(request, local_id):
    if request.method == "GET":
        return casoController.listarPorLocal(local_id)

def formasContagio(request):
    if request.method == "GET":
        return formaContagioController.listar()
