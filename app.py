from flask import Flask, jsonify
import flask_login as login
from flask_cors import CORS
from controller.user_controller import user_bp
from controller.consumo_controller import consumo_bp
from controller.dica_controller import dica_bp
from controller.meta_controller import meta_bp
from services import user_service

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
CORS(app)

login_manager = login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user_service.get_usuario(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Login required"}), 401

@app.route("/")
def index():
    return jsonify({"message": "API is running"})

# Registrando blueprints
app.register_blueprint(user_bp, url_prefix="/usuarios")
app.register_blueprint(consumo_bp, url_prefix="/consumos")
app.register_blueprint(dica_bp, url_prefix="/dicas")
app.register_blueprint(meta_bp, url_prefix="/metas")

if __name__ == "__main__":
    app.run(debug=True)