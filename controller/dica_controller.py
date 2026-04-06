from flask import Blueprint, request, jsonify
import flask_login as login
from services import dica_service

dica_bp = Blueprint("dica", __name__)

@dica_bp.route("/", methods=["GET", "POST"])
@login.login_required
def gerenciar_dicas():
    if request.method == "POST":
        data = request.get_json()
        dica = dica_service.criar_dica(data["titulo"], data["descricao"])
        return jsonify({"message": "Dica criada", "dica": {"id": dica.id, "titulo": dica.titulo, "descricao": dica.descricao}}), 201
    else:
        dicas = dica_service.listar_dicas()
        return jsonify([{"id": d.id, "titulo": d.titulo, "descricao": d.descricao} for d in dicas])
