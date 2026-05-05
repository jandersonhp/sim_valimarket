from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import json
import os
import uuid
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

ADMIN_CODE = os.environ.get('ACCESS_CODE')
PRODUTOS_FILE = os.path.join(os.path.dirname(__file__), 'produtos.json')
EMPRESAS_FILE = os.path.join(os.path.dirname(__file__), 'empresas.json')

def read_json(file_path, default):
    if not os.path.exists(file_path):
        return default
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return default

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_products():
    return read_json(PRODUTOS_FILE, [])

def write_products(products):
    write_json(PRODUTOS_FILE, products)

def read_empresas():
    return read_json(EMPRESAS_FILE, [])

def write_empresas(empresas):
    write_json(EMPRESAS_FILE, empresas)

def generate_access_code(nome_empresa):
    unique = f"{nome_empresa}-{uuid.uuid4().hex[:8].upper()}"
    return unique

def find_empresa_by_codigo(codigo):
    empresas = read_empresas()
    return next((e for e in empresas if e.get('codigoAcesso') == codigo), None)

@app.route('/empresas', methods=['POST'])
def create_empresa():
    data = request.get_json()
    if not data or data.get('adminCode') != ADMIN_CODE:
        return jsonify({'error': 'Acesso não autorizado'}), 403

    required = ['nome', 'telefone', 'endereco']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400

    empresas = read_empresas()
    access_code = generate_access_code(data['nome'])

    empresa = {
        'nome': data['nome'],
        'telefone': data['telefone'],
        'endereco': data['endereco'],
        'email': data.get('email', ''),
        'codigoAcesso': access_code
    }

    empresas.append(empresa)
    write_empresas(empresas)
    return jsonify(empresa), 201

@app.route('/empresas', methods=['GET'])
def list_empresas():
    return jsonify(read_empresas())

@app.route('/produtos', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    codigo = data.get('codigoAcesso')
    empresa_valida = find_empresa_by_codigo(codigo)

    if not empresa_valida:
        return jsonify({'error': 'Código de acesso inválido'}), 403

    required = ['nome', 'validade', 'preco', 'precoDesconto']
    for field in required:
        if field not in data or not data[field]:
            return jsonify({'error': f'Campo {field} é obrigatório'}), 400

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

    products = read_products()
    products.append(product)
    write_products(products)
    return jsonify(product), 201

@app.route('/produtos', methods=['GET'])
def list_products():
    return jsonify(read_products())

@app.route('/produtos/<product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    codigo = data.get('codigoAcesso')
    empresa_valida = find_empresa_by_codigo(codigo)

    if not empresa_valida:
        return jsonify({'error': 'Código de acesso inválido'}), 403

    products = read_products()
    product = next((p for p in products if p.get('id') == product_id), None)

    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404

    if product.get('empresa') != empresa_valida['nome']:
        return jsonify({'error': 'Não autorizado a editar este produto'}), 403

    # Atualizar campos permitidos
    if 'nome' in data:
        product['nome'] = data['nome']
    if 'validade' in data:
        product['validade'] = data['validade']
    if 'preco' in data:
        product['preco'] = float(data['preco'])
    if 'precoDesconto' in data:
        product['precoDesconto'] = float(data['precoDesconto'])

    write_products(products)
    return jsonify(product), 200

@app.route('/produtos/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    codigo = request.args.get('codigoAcesso')
    if not codigo:
        return jsonify({'error': 'Código de acesso necessário'}), 400

    empresa_valida = find_empresa_by_codigo(codigo)
    if not empresa_valida:
        return jsonify({'error': 'Código de acesso inválido'}), 403

    products = read_products()
    product = next((p for p in products if p.get('id') == product_id), None)

    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404

    if product.get('empresa') != empresa_valida['nome']:
        return jsonify({'error': 'Não autorizado a excluir este produto'}), 403

    products = [p for p in products if p.get('id') != product_id]
    write_products(products)
    return jsonify({'message': 'Produto excluído com sucesso'}), 200

@app.route('/empresa/produtos', methods=['GET'])
def list_empresa_products():
    codigo = request.args.get('codigoAcesso')
    if not codigo:
        return jsonify({'error': 'Código de acesso necessário'}), 400

    empresa_valida = find_empresa_by_codigo(codigo)
    if not empresa_valida:
        return jsonify({'error': 'Código de acesso inválido'}), 403

    products = read_products()
    empresa_products = [p for p in products if p.get('empresa') == empresa_valida['nome']]
    return jsonify(empresa_products)

@app.route('/produtos/proximos', methods=['GET'])
def list_near_expiry():
    products = read_products()
    today = datetime.now().date()
    three_days = today + timedelta(days=3)
    near_expiry = []
    for p in products:
        try:
            validade = datetime.strptime(p['validade'], '%Y-%m-%d').date()
            if validade <= three_days and validade >= today:
                near_expiry.append(p)
        except ValueError:
            continue
    return jsonify(near_expiry)

if __name__ == '__main__':
    if not os.path.exists(PRODUTOS_FILE):
        write_products([])
    if not os.path.exists(EMPRESAS_FILE):
        write_empresas([])
    app.run(debug=True, port=5000)
