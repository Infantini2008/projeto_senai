# Importação das bibliotecas necessárias
from flask import Flask, render_template, request, jsonify
import flask_login as login
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Chave secreta usada para assinar os cookies de sessão de forma segura (mude em produção)
app.secret_key = 'your_secret_key_here'

# Habilita o CORS para permitir que aplicações front-end (em outras portas/domínios) acessem esta API
CORS(app)
@app.route("/")
def home():
    return render_template('index.html')


# Configuração do gerenciador de login do Flask
login_manager = login.LoginManager()
login_manager.init_app(app)

# Define a resposta padrão caso um usuário não autenticado tente acessar uma rota protegida
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'error': 'Login required'}), 401

# --- BANCO DE DADOS EM MEMÓRIA ---
# Dicionários usados para armazenar os dados temporariamente (são perdidos ao reiniciar o servidor)
usuarios = {}
proximo_id_usuario = 1

consumos = {}
proximo_id_consumo = 1

dicas = {}
proximo_id_dica = 1

metas = {}
proximo_id_meta = 1

# --- MODELOS DE DADOS (CLASSES) ---

# Classe de Usuário que herda UserMixin (necessário para o flask_login funcionar)
class Usuario(login.UserMixin):
    def __init__(self, user_id, nome, email, senha_hash): # Corrigido para __init__
        self.id = str(user_id)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

class Consumo:
    def __init__(self, id, user_id, nome, valor): # Corrigido para __init__
        self.id = str(id)
        self.user_id = str(user_id)
        self.nome = nome
        self.valor = valor

class DicaEconomia:
    def __init__(self, id, titulo, descricao): # Corrigido para __init__
        self.id = str(id)
        self.titulo = titulo
        self.descricao = descricao

class Meta:
    def __init__(self, id, user_id, titulo, descricao): # Corrigido para __init__
        self.id = str(id)
        self.user_id = str(user_id)
        self.titulo = titulo
        self.descricao = descricao

# --- GERENCIAMENTO DE SESSÃO ---

# Função obrigatória do flask_login para recuperar o usuário logado a partir do seu ID
@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    # Busca o usuário no "banco de dados" em memória
    return usuarios.get(str(user_id))

# --- ROTAS DA API ---

# Rota raiz para testar se a API está no ar
@app.route('/')
def index():
    return jsonify({'message': 'API is running'})

# Rota para o usuário fazer login
@app.route('/login', methods=['POST'])
def login_usuario():
    # Pega os dados enviados no corpo da requisição em formato JSON
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados JSON inválidos ou ausentes'}), 400

    email = data.get('email')
    senha = data.get('senha')

    # Validação básica de preenchimento
    if not email or not senha:
        return jsonify({'error': 'Email e senha são obrigatórios'}), 400

    # Busca o usuário pelo e-mail no dicionário
    user = next((u for u in usuarios.values() if u.email == email), None)
    
    # Verifica se o usuário existe e se a senha enviada bate com a senha criptografada armazenada
    if not user or not check_password_hash(user.senha_hash, senha):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    # Registra a sessão do usuário no Flask-Login
    login.login_user(user)
    return jsonify({'message': 'Login realizado', 'user': {'id': user.id, 'nome': user.nome, 'email': user.email}})

# Rota para sair da conta (exige estar logado)
@app.route('/logout')
@login.login_required
def logout():
    # Encerra a sessão do usuário
    login.logout_user()
    return jsonify({'message': 'Logout realizado'})

# Rota para cadastrar um novo usuário
@app.route('/criar_usuario', methods=['POST'])
def criar_usuario_route():
    global proximo_id_usuario

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados JSON inválidos ou ausentes'}), 400

    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')

    # Validação dos dados
    if not nome or not email or not senha:
        return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400

    # Verifica se o e-mail já existe na base
    if any(user.email == email for user in usuarios.values()):
        return jsonify({'error': 'Email já cadastrado'}), 400

    # Criptografa a senha antes de salvar
    senha_hash = generate_password_hash(senha)
    
    # Instancia o usuário e salva no dicionário
    user = Usuario(user_id=proximo_id_usuario, nome=nome, email=email, senha_hash=senha_hash)
    usuarios[user.id] = user
    proximo_id_usuario += 1 # Incrementa o ID para o próximo cadastro

    # Retorna o status 201 (Created) e os dados do usuário (sem a senha)
    return jsonify({
        'message': 'Usuário criado',
        'user': {
            'id': user.id,
            'nome': user.nome,
            'email': user.email,
        },
    }), 201

# Rota para gerenciar os consumos (exige login)
@app.route('/consumos', methods=['GET', 'POST'])
@login.login_required
def gerenciar_consumos():
    global proximo_id_consumo
    # Pega o ID do usuário que está logado atualmente
    user_id = login.current_user.id

    # Se a requisição for POST, o usuário quer CRIAR um novo consumo
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados JSON inválidos ou ausentes'}), 400

        nome = data.get('nome')
        valor = data.get('valor')

        if not nome or valor is None:
            return jsonify({'error': 'Nome e valor são obrigatórios'}), 400

        # Cria o objeto de consumo associado ao ID do usuário e salva
        consumo = Consumo(id=proximo_id_consumo, user_id=user_id, nome=nome, valor=valor)
        consumos[consumo.id] = consumo
        proximo_id_consumo += 1

        return jsonify({
            'message': 'Consumo criado',
            'consumo': {
                'id': consumo.id,
                'nome': consumo.nome,
                'valor': consumo.valor,
            },
        }), 201

    # Se a requisição for GET, o usuário quer LER seus consumos
    else:
        # Filtra a lista de consumos para retornar apenas os que pertencem ao usuário logado
        user_consumos = [c for c in consumos.values() if c.user_id == user_id]
        return jsonify([{
            'id': c.id,
            'nome': c.nome,
            'valor': c.valor,
        } for c in user_consumos])

# Rota para gerenciar as dicas (exige login)
@app.route('/dicas', methods=['GET', 'POST'])
@login.login_required
def gerenciar_dicas():
    global proximo_id_dica

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados JSON inválidos ou ausentes'}), 400

        titulo = data.get('titulo')
        descricao = data.get('descricao')

        if not titulo or not descricao:
            return jsonify({'error': 'Título e descrição são obrigatórios'}), 400

        # Cria a dica e salva
        dica = DicaEconomia(id=proximo_id_dica, titulo=titulo, descricao=descricao)
        dicas[dica.id] = dica
        proximo_id_dica += 1

        return jsonify({
            'message': 'Dica criada',
            'dica': {
                'id': dica.id,
                'titulo': dica.titulo,
                'descricao': dica.descricao,
            },
        }), 201

    else:
        # Como as dicas não são vinculadas a um usuário específico, retorna todas para qualquer usuário logado
        return jsonify([{
            'id': d.id,
            'titulo': d.titulo,
            'descricao': d.descricao,
        } for d in dicas.values()])

# Rota para gerenciar as metas do usuário (exige login)
@app.route('/metas', methods=['GET', 'POST'])
@login.login_required
def gerenciar_metas():
    global proximo_id_meta
    user_id = login.current_user.id

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados JSON inválidos ou ausentes'}), 400

        titulo = data.get('titulo')
        descricao = data.get('descricao')

        if not titulo or not descricao:
            return jsonify({'error': 'Título e descrição são obrigatórios'}), 400

        # Cria a meta vinculada ao usuário logado e salva
        meta = Meta(id=proximo_id_meta, user_id=user_id, titulo=titulo, descricao=descricao)
        metas[meta.id] = meta
        proximo_id_meta += 1

        return jsonify({
            'message': 'Meta criada',
            'meta': {
                'id': meta.id,
                'titulo': meta.titulo,
                'descricao': meta.descricao,
            },
        }), 201

    else:
        # Filtra e retorna apenas as metas do usuário logado
        user_metas = [m for m in metas.values() if m.user_id == user_id]
        return jsonify([{
            'id': m.id,
            'titulo': m.titulo,
            'descricao': m.descricao,
        } for m in user_metas])

# Inicializa o servidor quando o arquivo é executado diretamente
if __name__ == '__main__':
    # O modo debug=True permite que o servidor reinicie sozinho quando você alterar o código
    app.run(debug=True)