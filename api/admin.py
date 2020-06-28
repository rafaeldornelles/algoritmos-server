from django.contrib import admin
from .models import Bairro, Locais, Paciente, FormaContagio, Sintoma, Caso

# Register your models here.
admin.site.register(Bairro)
admin.site.register(Locais)
admin.site.register(Paciente)
admin.site.register(FormaContagio)
admin.site.register(Sintoma)
admin.site.register(Caso)