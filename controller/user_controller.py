from flask import Blueprint, request, jsonify
import flask_login as login
from services import user_service

user_bp = Blueprint("user", __name__)

@user_bp.route("/criar_usuario", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    try:
        user = user_service.criar_usuario(data["nome"], data["email"], data["senha"])
        return jsonify({"message": "Usuário criado", "user": {"id": user.id, "nome": user.nome, "email": user.email}}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_bp.route("/login", methods=["POST"])
def login_usuario():
    data = request.get_json()
    user = user_service.autenticar_usuario(data["email"], data["senha"])
    if not user:
        return jsonify({"error": "Credenciais inválidas"}), 401
    login.login_user(user)
    return jsonify({"message": "Login realizado", "user": {"id": user.id, "nome": user.nome, "email": user.email}})

@user_bp.route("/logout")
@login.login_required
def logout():
    login.logout_user()
    return jsonify({"message": "Logout realizado"})
