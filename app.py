from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
import unicodedata
import re
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)  # Permite todas as origens (CORS aberto para dev)


ADMIN_CODE = os.environ.get('ACCESS_CODE')
MONGODB_URI = os.environ.get('MONGODB_URI')

mongo_client = None
db = None

def check_db():
    if db is None:
        return jsonify({'error': 'Servico temporariamente indisponivel. Tente novamente em instantes.'}), 503
    return None

if MONGODB_URI:
    try:
        from pymongo import MongoClient
        mongo_client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            tlsAllowInvalidCertificates=True
        )
        mongo_client.admin.command('ping')
        try:
            db = mongo_client.get_default_database()
        except:
            db = mongo_client['valimarket']
        print("MongoDB conectado com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar no MongoDB: {e}")
        mongo_client = None
        db = None
else:
    print("ERRO: MONGODB_URI nao definida.")

def find_empresa_by_codigo(codigo):
    return db.empresas.find_one({'codigoAcesso': codigo}, {'_id': 0})

def generate_access_code(nome_empresa):
    # Remove acentos
    nome_sem_acento = unicodedata.normalize('NFKD', nome_empresa).encode('ASCII', 'ignore').decode('ASCII')
    # Substitui espaços por hífen e remove caracteres especiais
    nome_limpo = nome_sem_acento.replace(' ', '-')
    unique = f"{nome_limpo}-{uuid.uuid4().hex[:8].upper()}"
    return unique

def sanitize_string(value, max_length=200):
    if not isinstance(value, str):
        return ''
    # Remove caracteres perigosos
    cleaned = re.sub(r'[<>"\';&]', '', value)
    return cleaned[:max_length]

def validate_phone(phone):
    if not phone:
        return False
    # Aceita apenas dígitos, parênteses, hífens, espaços e +
    if not re.match(r'^[\d\s\-\+\(\)]+$', phone):
        return False
    # Deve ter pelo menos 10 dígitos (DDD + número)
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10

@app.route('/empresas', methods=['POST'])
def create_empresa():
    db_check = check_db()
    if db_check:
        return db_check

    data = request.get_json()
    if not data or data.get('adminCode') != ADMIN_CODE:
        return jsonify({'error': 'Acesso nao autorizado'}), 403

    # Sanitização e validação
    nome = sanitize_string(data.get('nome', ''), 100)
    telefone = data.get('telefone', '')
    endereco = sanitize_string(data.get('endereco', ''), 200)
    email = sanitize_string(data.get('email', ''), 100)

    if not nome or not telefone or not endereco:
        return jsonify({'error': 'Campos obrigatorios: nome, telefone, endereco'}), 400

    if not validate_phone(telefone):
        return jsonify({'error': 'Telefone invalido'}), 400

    access_code = generate_access_code(nome)

    empresa = {
        'nome': nome,
        'telefone': telefone,
        'endereco': endereco,
        'email': email,
        'codigoAcesso': access_code
    }

    db.empresas.insert_one(empresa)
    result = {k: v for k, v in empresa.items() if k != '_id'}
    return jsonify(result), 201

@app.route('/empresas', methods=['GET'])
def list_empresas():
    db_check = check_db()
    if db_check:
        return db_check

    empresas = list(db.empresas.find({}, {'_id': 0}))
    safe_empresas = []
    for e in empresas:
        safe = {k: v for k, v in e.items() if k != 'codigoAcesso'}
        safe_empresas.append(safe)
    return jsonify(safe_empresas)

@app.route('/produtos', methods=['POST'])
def create_product():
    db_check = check_db()
    if db_check:
        return db_check

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados invalidos'}), 400

    codigo = data.get('codigoAcesso')
    empresa_valida = find_empresa_by_codigo(codigo)

    if not empresa_valida:
        return jsonify({'error': 'Codigo de acesso invalido'}), 403

    required = ['nome', 'validade', 'preco', 'precoDesconto']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} e obrigatorio'}), 400

    # Sanitização e validação
    nome = sanitize_string(data['nome'], 100)
    if not nome:
        return jsonify({'error': 'Nome invalido'}), 400

    # Validação de data YYYY-MM-DD
    validade = data['validade']
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', validade):
        return jsonify({'error': 'Validade deve ser YYYY-MM-DD'}), 400

    try:
        preco = float(data['preco'])
        precoDesconto = float(data['precoDesconto'])
        if preco <= 0 or precoDesconto < 0 or precoDesconto > preco:
            return jsonify({'error': 'Precos invalidos'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Precos devem ser numericos'}), 400

    product = {
        'id': str(uuid.uuid4()),
        'nome': nome,
        'empresa': empresa_valida['nome'],
        'validade': validade,
        'preco': preco,
        'precoDesconto': precoDesconto,
        'telefone': empresa_valida['telefone'],
        'endereco': empresa_valida['endereco']
    }

    db.produtos.insert_one(product)
    result = {k: v for k, v in product.items() if k != '_id'}
    return jsonify(result), 201

@app.route('/produtos', methods=['GET'])
def list_products():
    db_check = check_db()
    if db_check:
        return db_check
    return jsonify(list(db.produtos.find({}, {'_id': 0})))

@app.route('/produtos/<product_id>', methods=['PUT'])
def update_product(product_id):
    db_check = check_db()
    if db_check:
        return db_check
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados invalidos'}), 400

    codigo = data.get('codigoAcesso')
    empresa_valida = find_empresa_by_codigo(codigo)

    if not empresa_valida:
        return jsonify({'error': 'Codigo de acesso invalido'}), 403

    product = db.produtos.find_one({'id': product_id})
    if not product:
        return jsonify({'error': 'Produto nao encontrado'}), 404

    if product.get('empresa') != empresa_valida['nome']:
        return jsonify({'error': 'Nao autorizado a editar este produto'}), 403

    update_fields = {}
    if 'nome' in data:
        nome = sanitize_string(data['nome'], 100)
        if nome:
            update_fields['nome'] = nome
    if 'validade' in data:
        validade = data['validade']
        if re.match(r'^\d{4}-\d{2}-\d{2}$', validade):
            update_fields['validade'] = validade
    if 'preco' in data:
        try:
            update_fields['preco'] = float(data['preco'])
        except (ValueError, TypeError):
            pass
    if 'precoDesconto' in data:
        try:
            update_fields['precoDesconto'] = float(data['precoDesconto'])
        except (ValueError, TypeError):
            pass

    if update_fields:
        db.produtos.update_one({'id': product_id}, {'$set': update_fields})

    updated = db.produtos.find_one({'id': product_id}, {'_id': 0})
    return jsonify(updated), 200

@app.route('/produtos/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    db_check = check_db()
    if db_check:
        return db_check
    data = request.get_json()
    codigo = data.get('codigoAcesso') if data else None
    if not codigo:
        return jsonify({'error': 'Codigo de acesso necessario'}), 400

    empresa_valida = find_empresa_by_codigo(codigo)
    if not empresa_valida:
        return jsonify({'error': 'Codigo de acesso invalido'}), 403

    product = db.produtos.find_one({'id': product_id})
    if not product:
        return jsonify({'error': 'Produto nao encontrado'}), 404

    if product.get('empresa') != empresa_valida['nome']:
        return jsonify({'error': 'Nao autorizado a excluir este produto'}), 403

    db.produtos.delete_one({'id': product_id})
    return jsonify({'message': 'Produto excluido com sucesso'}), 200

@app.route('/empresa/produtos', methods=['GET'])
def list_empresa_products():
    db_check = check_db()
    if db_check:
        return db_check
    # Aceita tanto query param quanto JSON body
    codigo = request.args.get('codigoAcesso') or (request.get_json() or {}).get('codigoAcesso')
    if not codigo:
        return jsonify({'error': 'Codigo de acesso necessario'}), 400

    empresa_valida = find_empresa_by_codigo(codigo)
    if not empresa_valida:
        return jsonify({'error': 'Codigo de acesso invalido'}), 403

    products = list(db.produtos.find({'empresa': empresa_valida['nome']}, {'_id': 0}))
    return jsonify(products)

@app.route('/produtos/proximos', methods=['GET'])
def list_near_expiry():
    db_check = check_db()
    if db_check:
        return db_check
    products = list(db.produtos.find({}, {'_id': 0}))
    today = datetime.now().date()
    three_days = today + timedelta(days=3)
    near_expiry = []
    for p in products:
        try:
            validade = datetime.strptime(p['validade'], '%Y-%m-%d').date()
            if today <= validade <= three_days:
                near_expiry.append(p)
        except ValueError:
            continue
    return jsonify(near_expiry)

@app.route('/admin/empresas', methods=['DELETE'])
def delete_empresa_admin():
    db_check = check_db()
    if db_check:
        return db_check

    data = request.get_json()
    if not data or data.get('adminCode') != ADMIN_CODE:
        return jsonify({'error': 'Acesso nao autorizado'}), 403

    nome = data.get('nome')
    telefone = data.get('telefone')
    if not nome or not telefone:
        return jsonify({'error': 'nome e telefone sao obrigatorios'}), 400

    # Remove produtos da empresa
    db.produtos.delete_many({'empresa': nome})
    # Remove a empresa
    result = db.empresas.delete_one({'nome': nome, 'telefone': telefone})

    if result.deleted_count == 0:
        return jsonify({'error': 'Empresa nao encontrada'}), 404

    return jsonify({'message': 'Empresa excluida com sucesso'}), 200

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = not os.environ.get('RENDER')
    use_reloader = False if os.name == 'nt' else debug_mode
    app.run(debug=debug_mode, port=port, host='0.0.0.0', use_reloader=use_reloader)
