let allProducts = [];
let allCompanies = [];
let currentFilter = 'all';

function formatDate(isoDate) {
    if (typeof isoDate === 'string' && isoDate.match(/^\d{4}-\d{2}-\d{2}$/)) {
        const parts = isoDate.split('-');
        return parts[2] + '/' + parts[1] + '/' + parts[0].slice(-2);
    }
    const date = new Date(isoDate);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);
    return day + '/' + month + '/' + year;
}

function createWhatsAppLink(phone) {
    const cleaned = phone.replace(/\D/g, '');
    const withCountry = cleaned.startsWith('55') ? cleaned : '55' + cleaned;
    return 'https://wa.me/' + withCountry;
}

function isNearExpiry(validade) {
    const parts = validade.split('-');
    const expiry = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const threeDays = new Date(today);
    threeDays.setDate(today.getDate() + 3);
    return expiry >= today && expiry <= threeDays;
}

function isExpired(validade) {
    const parts = validade.split('-');
    const expiry = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]));
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return expiry < today;
}

function renderProducts(products) {
    const container = document.getElementById('products-container');
    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #718096; grid-column: 1/-1;">Nenhum produto encontrado.</p>';
        return;
    }

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';

        const validade = formatDate(product.validade);
        const whatsappLink = createWhatsAppLink(product.telefone);
        const nearExpiry = isNearExpiry(product.validade);
        const expired = isExpired(product.validade);
        const discount = Math.round(((product.preco - product.precoDesconto) / product.preco) * 100);

        let priceHtml = '';
        if (nearExpiry) {
            priceHtml = '<div class="price">' +
                '<span class="original-price">R$ ' + product.preco.toFixed(2) + '</span>' +
                '<span class="discount-price">R$ ' + product.precoDesconto.toFixed(2) + '</span>' +
                '<span style="background: #f59e0b; color: white; padding: 4px 10px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin-left: 8px;">' + discount + '% OFF</span>' +
                '</div>';
        } else {
            priceHtml = '<div class="price">' +
                '<span class="normal-price">Preço: R$ ' + product.preco.toFixed(2) + '</span>' +
                '</div>';
        }

        card.innerHTML = '<h3>' + (expired ? '<s>' + product.nome + '</s> (Vencido)' : product.nome) + '</h3>' +
            '<p class="empresa">' + product.empresa + '</p>' +
            priceHtml +
            '<p class="validade ' + (nearExpiry ? 'near-expiry' : '') + (expired ? ' style="text-decoration: line-through;"' : '') + '">Validade: ' + validade + '</p>' +
            '<p class="address">📍 ' + product.endereco + '</p>' +
            (expired ? '' : '<a href="' + whatsappLink + '" target="_blank" class="whatsapp-btn">📞 WhatsApp</a>');

        container.appendChild(card);
    });
}

function populateCompanies(companies) {
    const select = document.getElementById('company-select');
    companies.forEach(company => {
        const option = document.createElement('option');
        option.value = company.nome;
        option.textContent = company.nome;
        select.appendChild(option);
    });
}

function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const selectedCompany = document.getElementById('company-select').value;
    let filtered = allProducts;

    // Remove produtos vencidos da visualização pública
    filtered = filtered.filter(p => !isExpired(p.validade));

    if (currentFilter === 'near') {
        filtered = filtered.filter(p => isNearExpiry(p.validade));
    }

    if (selectedCompany) {
        filtered = filtered.filter(p => p.empresa === selectedCompany);
    }

    if (searchTerm) {
        filtered = filtered.filter(p =>
            p.nome.toLowerCase().includes(searchTerm) ||
            p.empresa.toLowerCase().includes(searchTerm)
        );
    }

    renderProducts(filtered);
}

async function fetchProducts() {
    try {
        const response = await fetch('/produtos');
        allProducts = await response.json();
        applyFilters();
    } catch (error) {
        console.error('Erro ao buscar produtos:', error);
        const container = document.getElementById('products-container');
        container.innerHTML = '<p style="text-align: center; color: #e53e3e; grid-column: 1/-1;">Erro ao carregar produtos. Verifique se o backend está rodando.</p>';
    }
}

async function fetchCompanies() {
    try {
        const response = await fetch('/empresas');
        allCompanies = await response.json();
        populateCompanies(allCompanies);
    } catch (error) {
        console.error('Erro ao buscar empresas:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentFilter = tab.dataset.filter;
            applyFilters();
        });
    });

    document.getElementById('search-input').addEventListener('input', applyFilters);
    document.getElementById('company-select').addEventListener('change', applyFilters);

    fetchProducts();
    fetchCompanies();
    // Removido o setInterval para não interromper o usuário
});
