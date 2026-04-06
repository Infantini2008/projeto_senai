from flask import Blueprint, request, jsonify
import flask_login as login
from services import metas_services as meta_service

meta_bp = Blueprint("meta", __name__)

@meta_bp.route("/", methods=["GET", "POST"])
@login.login_required
def gerenciar_metas():
    user_id = login.current_user.id
    if request.method == "POST":
        data = request.get_json()
        meta = meta_service.criar_meta(user_id, data["titulo"], data["descricao"])
        return jsonify({"message": "Meta criada", "meta": {"id": meta.id, "titulo": meta.titulo, "descricao": meta.descricao}}), 201
    else:
        metas = meta_service.listar_metas(user_id)
        return jsonify([{"id": m.id, "titulo": m.titulo, "descricao": m.descricao} for m in metas])