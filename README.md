# ValiMarket 🛒

> Vitrine digital para produtos próximos do vencimento com desconto.

O **ValiMarket** é um MVP (Minimum Viable Product) desenvolvido para conectar comerciantes que precisam vender produtos próximos ao vencimento com desconto a clientes que buscam ofertas.

## 🎯 Objetivo

Criar uma plataforma simples, funcional e profissional que demonstre valor real para comerciantes (mercados, padarias, farmácias) e clientes, servindo como portal de entrada para validação de negócio.

## ✨ Tecnologias Utilizadas

- **Backend**: Python 3 + Flask (API RESTful)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Persistência**: Arquivos JSON (sem banco de dados complexo)
- **Deploy**: Render.com (100% gratuito)

## 🚀 Funcionalidades

### Para Clientes
- Visualização de todos os produtos disponíveis
- Filtro por **"Todos"** ou **"Com Desconto (3 dias)"**
- Busca por nome de produto ou empresa
- Filtro por empresa específica (dropdown)
- Botão direto para **WhatsApp** do comércio
- Design **mobile-first** (otimizado para celular)

### Para Empresas
- **Painel completo** com acesso via código único
- Cadastro simplificado de produtos (apenas 4 campos - dados da empresa são preenchidos automaticamente)
- **Edição e exclusão** de produtos cadastrados
- Mensagens de status visuais (sucesso/erro)

### Para Administradores
- Cadastro seguro de novas empresas
- Geração automática de códigos de acesso únicos
- Proteção por senha de admin (via variável de ambiente)

## 🔧 Segurança e Boas Práticas

- ✅ Código de admin via variável de ambiente (`.env` - nunca vai para o Git)
- ✅ Códigos de acesso únicos por empresa (gerados automaticamente)
- ✅ Validação de permissões (empresa só edita/exclui seus próprios produtos)
- ✅ `.gitignore` configurado para proteger dados sensíveis
- ✅ CORS habilitado para integração segura

## 📁 Estrutura do Projeto

```
sim_valimarket/
├── .gitignore
├── README.md
├── backend/
│   ├── app.py              # API Flask (rotas GET, POST, PUT, DELETE)
│   ├── empresas.json        # Dados das empresas cadastradas
│   ├── produtos.json        # Dados dos produtos
│   ├── .env                # Variáveis de ambiente (NUNCA commitado)
│   ├── .env.example         # Modelo de configuração
│   └── requirements.txt     # Dependências Python
└── frontend/
    ├── index.html           # Página inicial (foco em "Ver Ofertas")
    ├── cliente.html         # Vitrine de produtos para clientes
    ├── empresa.html         # Painel completo da empresa
    ├── admin.html           # Cadastro de novas empresas (admin)
    ├── empresa-dashboard.js # Lógica do painel da empresa
    ├── script.js            # Lógica da vitrine cliente
    ├── style.css            # Estilos globais (mobile-first)
    └── assets/
        └── favicon.png     # Ícone do site
```

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/sim_valimarket.git
cd sim_valimarket
```

### 2. Configurar o Backend
```bash
cd backend
cp .env.example .env
# Edite o .env e defina sua senha de admin
pip install -r requirements.txt
python app.py
```
O backend rodará em `http://localhost:5000`.

### 3. Acessar o Frontend
Abra `frontend/index.html` no navegador.

## 🌐 Deploy (100% Gratuito no Render)

### Backend (Web Service)
1. Acesse [Render.com](https://render.com) e crie uma conta
2. **New +** → **Web Service**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: valimarket-backend
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free
5. Adicione a variável de ambiente:
   - Key: `ACCESS_CODE` | Value: `sua_senha_aqui`
6. Clique em **Create Web Service**

### Frontend (Static Site)
1. No Render, **New +** → **Static Site**
2. Conecte o mesmo repositório
3. Configure:
   - **Name**: valimarket-frontend
   - **Root Directory**: `frontend`
   - **Publish Directory**: `.`
4. Clique em **Create Static Site**

### Atualizar URLs
Após o deploy, atualize as URLs da API nos arquivos:
- `frontend/script.js`
- `frontend/empresa-dashboard.js`
- `frontend/admin.html`

Altere `http://localhost:5000` para a URL do seu backend no Render.

## 📋 Exemplo de Uso

### Fluxo do Administrador
1. Acesse `frontend/admin.html`
2. Digite a senha de admin
3. Cadastre uma nova empresa (dados: nome, WhatsApp, endereço)
4. O sistema gera um **código único** (ex: `PADARIA-NOVA-ABC123`)
5. Envie o código para a empresa via WhatsApp

### Fluxo da Empresa
1. Acesse `frontend/empresa.html`
2. Digite o código recebido
3. Escolha **"Cadastrar Produto"** → Preencha: nome, validade, preço original, preço com desconto
4. Ou escolha **"Gerenciar Produtos"** → Edite ou exclua itens

### Fluxo do Cliente
1. Acesse `frontend/cliente.html`
2. Veja todas as ofertas ou filtre por "Com Desconto (3 dias)"
3. Busque por produto ou empresa
4. Clique no botão do **WhatsApp** para contatar o comércio

## ⚠️ Aviso Importante

> Os produtos devem ser confirmados diretamente no estabelecimento. Os preços podem variar.

## 🎨 Design e UX

- **Mobile-first**: 80%+ dos usuários acessarão via celular
- **Cores suaves**: Verde (#38a169) transmite confiança e frescor
- **Cards modernos**: Sombras suaves, bordas arredondadas
- **Navegação intuitiva**: Foco total no botão "Ver Ofertas"
- **Feedback visual**: Mensagens de sucesso/erro integradas (sem alerts irritantes)

## 📈 Status do Projeto

✅ MVP Completo e Funcional  
✅ Pronto para apresentação a comerciantes reais  
✅ Deploy gratuito configurado  
✅ Estrutura limpa para portfolio  

## 🔮 Sobre o Autor

Projeto desenvolvido como MVP para validação de negócio no setor de varejo, focando em redução de desperdício de alimentos através de uma solução digital simples e eficaz.

---

**Licença**: MIT  
**Contato**: [Seu Email/LinkedIn]
# Test
