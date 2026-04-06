import flask_login as login

class Usuario(login.UserMixin):
    def __init__(self, user_id, nome, email, senha_hash):
        self.id = str(user_id)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

class Consumo:
    def __init__(self, id, user_id, nome, valor):
        self.id = str(id)
        self.user_id = str(user_id)
        self.nome = nome
        self.valor = valor

class DicaEconomia:
    def __init__(self, id, titulo, descricao):
        self.id = str(id)
        self.titulo = titulo
        self.descricao = descricao

class Meta:
    def __init__(self, id, user_id, titulo, descricao):
        self.id = str(id)
        self.user_id = str(user_id)
        self.titulo = titulo
        self.descricao = descricao
