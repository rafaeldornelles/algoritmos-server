from django.urls import path

from . import views

urlpatterns = [
    path('bairros', views.bairros, name='bairros'), #GET ONLY

    path('locais', views.locais, name='locais'), #GET E POST

    path('pacientes', views.pacientes, name='pacientes'), #GET E POST
    path('pacientes/<int:paciente_id>', views.paciente, name='paciente'), #GET PUT E DELETE

    path('sintomas', views.sintomas, name='sintomas'), #GET ONLY

    path('casos', views.casos, name='bairros'), #GET E POST
    path('casos/<int:caso_id>', views.caso, name='caso'), #GET PUT E DELETE
    path('casos/bairro/<int:bairro_id>', views.casosPorBairro, name='casosporbairro'), #GET
    path('casos/local/<int:local_id>', views.casosPorLocalVisitado, name='casosporlocalvisitado'), #GET

    path('formascontagio', views.formasContagio, name='formascontagio') #GET ONLY
]