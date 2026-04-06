from werkzeug.security import generate_password_hash, check_password_hash
from Models.Model.schemas import Usuario
usuarios = {}
proximo_id_usuario = 1

def criar_usuario(nome, email, senha):
    global proximo_id_usuario
    if any(user.email == email for user in usuarios.values()):
        raise ValueError("Email já cadastrado")

    senha_hash = generate_password_hash(senha)
    user = Usuario(user_id=proximo_id_usuario, nome=nome, email=email, senha_hash=senha_hash)
    usuarios[user.id] = user
    proximo_id_usuario += 1
    return user

def autenticar_usuario(email, senha):
    user = next((u for u in usuarios.values() if u.email == email), None)
    if not user or not check_password_hash(user.senha_hash, senha):
        return None
    return user

def get_usuario(user_id):
    return usuarios.get(str(user_id))
