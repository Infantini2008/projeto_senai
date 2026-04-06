from Models.Model.schemas import Consumo

consumos = {}
proximo_id_consumo = 1

def criar_consumo(user_id, nome, valor):
    global proximo_id_consumo
    consumo = Consumo(id=proximo_id_consumo, user_id=user_id, nome=nome, valor=valor)
    consumos[consumo.id] = consumo
    proximo_id_consumo += 1
    return consumo

def listar_consumos(user_id):
    return [c for c in consumos.values() if c.user_id == user_id]