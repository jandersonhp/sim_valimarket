let allProducts = [];
let allCompanies = [];
let currentFilter = 'all';

function formatDate(isoDate) {
    const date = new Date(isoDate);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);
    return day + '/' + month + '/' + year;
}

function createWhatsAppLink(phone) {
    const cleaned = phone.replace(/\D/g, '');
    return 'https://wa.me/' + cleaned;
}

function isNearExpiry(validade) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const threeDays = new Date(today);
    threeDays.setDate(today.getDate() + 3);
    const expiry = new Date(validade);
    return expiry >= today && expiry <= threeDays;
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

        let priceHtml = '';
        if (nearExpiry) {
            priceHtml = '<div class="price">' +
                '<span class="original-price">R$ ' + product.preco.toFixed(2) + '</span>' +
                '<span class="discount-price">R$ ' + product.precoDesconto.toFixed(2) + '</span>' +
                '</div>';
        } else {
            priceHtml = '<div class="price">' +
                '<span class="normal-price">Preço: R$ ' + product.preco.toFixed(2) + '</span>' +
                '</div>';
        }

        card.innerHTML = '<h3>' + product.nome + '</h3>' +
            '<p class="empresa">' + product.empresa + '</p>' +
            priceHtml +
            '<p class="validade ' + (nearExpiry ? 'near-expiry' : '') + '">Validade: ' + validade + '</p>' +
            '<p class="address">📍 ' + product.endereco + '</p>' +
            '<a href="' + whatsappLink + '" target="_blank" class="whatsapp-btn">📞 WhatsApp</a>';

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
    setInterval(fetchProducts, 60000);
});
