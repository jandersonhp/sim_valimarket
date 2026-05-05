let currentCodigo = "";
function showError(elementId, msg) {
    const el = document.getElementById(elementId);
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4000);
}

function showStatus(title, text, isSuccess) {
    const msgEl = document.getElementById('status-message');
    const titleEl = document.getElementById('status-title');
    const textEl = document.getElementById('status-text');
    
    titleEl.textContent = title;
    textEl.textContent = text;
    msgEl.className = 'status-message ' + (isSuccess ? 'success' : '');
    msgEl.style.display = 'block';
    alert('STATUS: ' + title + ' - ' + text);
    
    setTimeout(() => {
        msgEl.style.display = 'none';
    }, 3000);
}

async function accessPanel() {
    const codigo = document.getElementById('codigo-input').value;
    if (!codigo) {
        showError('error-message', 'Digite seu código de acesso');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/empresa/produtos?codigoAcesso=' + encodeURIComponent(codigo));
        if (!response.ok) {
            const error = await response.json();
            showError('error-message', error.error);
            return;
        }
        currentCodigo = codigo;
        document.getElementById('access-panel').style.display = 'none';
        document.getElementById('options').style.display = 'grid';
        document.getElementById('codigoAcesso').value = codigo;
    } catch (error) {
        showError('error-message', 'Erro ao conectar com o servidor');
    }
}

function showOptions() {
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('products-list').style.display = 'none';
    document.getElementById('options').style.display = 'grid';
    // Keep status message visible
    const statusMsg = document.getElementById('status-message');
    if (statusMsg.textContent) {
        statusMsg.style.display = 'block';
    }
}

function showRegisterForm(product = null) {
    document.getElementById('options').style.display = 'none';
    document.getElementById('products-list').style.display = 'none';
    document.getElementById('register-form').style.display = 'block';
    
    if (product) {
        document.getElementById('form-title').textContent = 'Editar Produto';
        document.getElementById('productId').value = product.id;
        document.getElementById('nome').value = product.nome;
        document.getElementById('validade').value = product.validade;
        document.getElementById('preco').value = product.preco;
        document.getElementById('precoDesconto').value = product.precoDesconto;
        document.getElementById('submit-btn').textContent = 'Atualizar Produto';
    } else {
        document.getElementById('form-title').textContent = 'Cadastrar Produto';
        document.getElementById('productId').value = '';
        document.getElementById('product-form').reset();
        document.getElementById('codigoAcesso').value = currentCodigo;
        document.getElementById('submit-btn').textContent = 'Cadastrar Produto';
    }
}

async function showManageProducts() {
    document.getElementById('options').style.display = 'none';
    document.getElementById('register-form').style.display = 'none';
    document.getElementById('products-list').style.display = 'block';
    // Keep status message visible
    const statusMsg = document.getElementById('status-message');
    if (statusMsg.textContent) {
        statusMsg.style.display = 'block';
    }


    try {
        const response = await fetch('http://localhost:5000/empresa/produtos?codigoAcesso=' + encodeURIComponent(currentCodigo));
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        showStatus('Erro!', 'Erro ao carregar produtos', false);
    }
}

function formatDate(isoDate) {
    const date = new Date(isoDate);
    const d = date.getDate();
    const m = date.getMonth() + 1;
    const y = date.getFullYear().toString().slice(-2);
    const day = d < 10 ? '0' + d : d;
    const month = m < 10 ? '0' + m : m;
    return day + '/' + month + '/' + y;
}

function displayProducts(products) {
    const container = document.getElementById('products-container');
    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = '<p style="text-align:center; color:#718096; padding:2rem;">Nenhum produto cadastrado ainda.</p>';
        return;
    }

    products.forEach(product => {
        const item = document.createElement('div');
        item.className = 'product-item';
        const validade = formatDate(product.validade);

        const editBtn = document.createElement('button');
        editBtn.className = 'btn-edit';
        editBtn.textContent = 'Editar';
        editBtn.onclick = function() { editProduct(product); };

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn-delete';
        deleteBtn.textContent = 'Excluir';
        deleteBtn.onclick = function() { deleteProduct(product.id); };

        item.innerHTML = '<div class="details">' +
            '<h3>' + product.nome + '</h3>' +
            '<p>Validade: ' + validade + ' | Preço: R$ ' + product.preco.toFixed(2) + ' | Desconto: R$ ' + product.precoDesconto.toFixed(2) + '</p>' +
            '</div>';

        const actions = document.createElement('div');
        actions.className = 'product-actions';
        actions.appendChild(editBtn);
        actions.appendChild(deleteBtn);

        item.appendChild(actions);
        container.appendChild(item);
    });
}

function editProduct(product) {
    showRegisterForm(product);
}

async function deleteProduct(productId) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) return;

    try {
        const response = await fetch('http://localhost:5000/produtos/' + productId + '?codigoAcesso=' + encodeURIComponent(currentCodigo), {
            method: 'DELETE'
        });

        if (response.ok) {
            showStatus('Produto Excluído!', 'O produto foi removido com sucesso.', true);
            showManageProducts();
        } else {
            const error = await response.json();
            showStatus('Erro!', error.error, false);
        }
    } catch (error) {
        showStatus('Erro!', 'Erro ao conectar com o servidor', false);
    }
}

document.getElementById('product-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const productId = form.productId.value;
    const data = {
        codigoAcesso: currentCodigo,
        nome: form.nome.value,
        validade: form.validade.value,
        preco: form.preco.value,
        precoDesconto: form.precoDesconto.value
    };

    try {
        let response;
        if (productId) {
            response = await fetch('http://localhost:5000/produtos/' + productId, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        } else {
            response = await fetch('http://localhost:5000/produtos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
        }

        if (response.ok) {
            const action = productId ? 'atualizado' : 'cadastrado';
            showStatus('Sucesso!', 'Produto ' + action + ' com sucesso!', true);
            document.getElementById('register-form').style.display = 'none';
            showManageProducts();
        } else {
            const error = await response.json();
            showError('form-error', error.error);
        }
    } catch (error) {
        showError('form-error', 'Erro ao conectar com o servidor.');
    }
});
