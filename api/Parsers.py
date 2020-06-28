from .models import Bairro, Locais, Paciente, FormaContagio, Sintoma, Caso


class Parsers:
    def bairroToDict(self, bairro:Bairro):
        return {
            "id": bairro.id,
            "descricao": bairro.descricao
        }

    def bairrosToDict(self, bairros:[Bairro]):
        return [self.bairroToDict(bairro) for bairro in bairros]

    def localToDict(self, local:Locais):
        return {
            "id":local.id,
            "nome":local.nome,
            "endereco":local.endereco
        }

    def locaisToDict(self, locais:[Locais]):
        return [self.localToDict(local) for local in locais]

    def pacienteToDict(self, paciente:Paciente):
        return {
            "id": paciente.id,
            "nome": paciente.nome,
            "bairro": self.bairroToDict(paciente.bairro),
            "locaisVisitados": self.locaisToDict(paciente.locaisVisitados.all())
        }

    def pacientesToDict(self, pacientes: [Paciente]):
        return [self.pacienteToDict(paciente) for paciente in pacientes]

    def formaContagioToDict(self, forma:FormaContagio):
        return{
            "id": forma.id,
            "descricao":forma.descricao
        }

    def formasContagioToDict(self, formas:[FormaContagio]):
        return [self.formaContagioToDict(forma) for forma in formas]

    def sintomaToDict(self, sintoma:Sintoma):
        return{
            "id": sintoma.id,
            "descricao": sintoma.descricao
        }

    def sintomasToDict(self, sintomas:[Sintoma]):
        return [self.sintomaToDict(sintoma) for sintoma in sintomas]

    def casoToDict(self, caso: Caso):
        dataFimSintomas = None
        try:
            dataFimSintomas = caso.dataFimSintomas.strftime('%Y-%m-%d')
        except:
            pass

        return {
            "id": caso.id,
            "paciente": self.pacienteToDict(caso.paciente),
            "formaContagio": self.formaContagioToDict(caso.formaContagio),
            "dataInicioSintomas": caso.dataInicioSintomas.strftime('%Y-%m-%d'),
            "dataRelato": caso.dataRelato.strftime('%Y-%m-%d'),
            "dataFimSintomas": dataFimSintomas,
            "sintomas": self.sintomasToDict(caso.sintomas.all())
        }

    def casosToDict(self, casos: [Caso]):
        return [self.casoToDict(caso) for caso in casos]
