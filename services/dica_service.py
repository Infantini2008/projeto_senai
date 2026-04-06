from Models.Model.schemas import DicaEconomia

dicas = {}
proximo_id_dica = 1

def criar_dica(titulo, descricao):
    global proximo_id_dica
    dica = DicaEconomia(id=proximo_id_dica, titulo=titulo, descricao=descricao)
    dicas[dica.id] = dica
    proximo_id_dica += 1
    return dica

def listar_dicas():
    return list(dicas.values())
