from main.models.schemas import Meta

metas = {}
proximo_id_meta = 1

def criar_meta(user_id, titulo, descricao):
    global proximo_id_meta
    meta = Meta(id=proximo_id_meta, user_id=user_id, titulo=titulo, descricao=descricao)
    metas[meta.id] = meta
    proximo_id_meta += 1
    return meta

def listar_metas(user_id):
    return [m for m in metas.values() if m.user_id == user_id]
