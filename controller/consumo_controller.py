from flask import Blueprint, request, jsonify
import flask_login as login
from services import consumo_service

consumo_bp = Blueprint("consumo", __name__)

@consumo_bp.route("/", methods=["GET", "POST"])
@login.login_required
def gerenciar_consumos():
    user_id = login.current_user.id
    if request.method == "POST":
        data = request.get_json()
        consumo = consumo_service.criar_consumo(user_id, data["nome"], data["valor"])
        return jsonify({"message": "Consumo criado", "consumo": {"id": consumo.id, "nome": consumo.nome, "valor": consumo.valor}}), 201
    else:
        consumos = consumo_service.listar_consumos(user_id)
        return jsonify([{"id": c.id, "nome": c.nome, "valor": c.valor} for c in consumos])
