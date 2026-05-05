from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import uuid
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

ADMIN_CODE = os.environ.get('ACCESS_CODE')
MONGODB_URI = os.environ.get('MONGODB_URI')

if not MONGODB_URI:
    print("ERRO: MONGODB_URI nao definida. Configure a variavel de ambiente.")
    exit(1)

try:
    from pymongo import MongoClient
    mongo_client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    try:
        db = mongo_client.get_default_database()
    except:
        db = mongo_client['valimarket']
    print("MongoDB conectado com sucesso!")
except Exception as e:
    print(f"Erro ao conectar no MongoDB: {e}")
    exit(1)

def find_empresa_by_codigo(codigo):
    return db.empresas.find_one({'codigoAcesso': codigo}, {'_id': 0})

def generate_access_code(nome_empresa):
    unique = f"{nome_empresa}-{uuid.uuid4().hex[:8].upper()}"
    return unique

@app.route('/empresas', methods=['POST'])
def create_empresa():
    data = request.get_json()
    if not data or data.get('adminCode') != ADMIN_CODE:
        return jsonify({'error': 'Acesso nao autorizado'}), 403

    required = ['nome', 'telefone', 'endereco']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} e obrigatorio'}), 400

    access_code = generate_access_code(data['nome'])

    empresa = {
        'nome': data['nome'],
        'telefone': data['telefone'],
        'endereco': data['endereco'],
        'email': data.get('email', ''),
        'codigoAcesso': access_code
    }

    db.empresas.insert_one(empresa)
    result = {k: v for k, v in empresa.items() if k != '_id'}
    return jsonify(result), 201

@app.route('/empresas', methods=['GET'])
def list_empresas():
    empresas = list(db.empresas.find({}, {'_id': 0}))
    safe_empresas = []
    for e in empresas:
        safe = {k: v for k, v in e.items() if k != 'codigoAcesso'}
        safe_empresas.append(safe)
    return jsonify(safe_empresas)

@app.route('/produtos', methods=['POST'])
def create_product():
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

    product = {
        'id': str(uuid.uuid4()),
        'nome': data['nome'],
        'empresa': empresa_valida['nome'],
        'validade': data['validade'],
        'preco': float(data['preco']),
        'precoDesconto': float(data['precoDesconto']),
        'telefone': empresa_valida['telefone'],
        'endereco': empresa_valida['endereco']
    }

    db.produtos.insert_one(product)
    result = {k: v for k, v in product.items() if k != '_id'}
    return jsonify(result), 201

@app.route('/produtos', methods=['GET'])
def list_products():
    return jsonify(list(db.produtos.find({}, {'_id': 0})))

@app.route('/produtos/<product_id>', methods=['PUT'])
def update_product(product_id):
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
        update_fields['nome'] = data['nome']
    if 'validade' in data:
        update_fields['validade'] = data['validade']
    if 'preco' in data:
        update_fields['preco'] = float(data['preco'])
    if 'precoDesconto' in data:
        update_fields['precoDesconto'] = float(data['precoDesconto'])

    if update_fields:
        db.produtos.update_one({'id': product_id}, {'$set': update_fields})

    updated = db.produtos.find_one({'id': product_id}, {'_id': 0})
    return jsonify(updated), 200

@app.route('/produtos/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    codigo = request.args.get('codigoAcesso')
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
    codigo = request.args.get('codigoAcesso')
    if not codigo:
        return jsonify({'error': 'Codigo de acesso necessario'}), 400

    empresa_valida = find_empresa_by_codigo(codigo)
    if not empresa_valida:
        return jsonify({'error': 'Codigo de acesso invalido'}), 403

    products = list(db.produtos.find({'empresa': empresa_valida['nome']}, {'_id': 0}))
    return jsonify(products)

@app.route('/produtos/proximos', methods=['GET'])
def list_near_expiry():
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
