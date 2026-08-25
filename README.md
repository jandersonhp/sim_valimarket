# ValiMarket 🛒

> Menos desperdício pra quem vende, mais economia pra quem compra.

O **ValiMarket** é um MVP (Minimum Viable Product) desenvolvido para conectar comércios que precisam vender produtos próximos ao vencimento com desconto a consumidores que buscam ofertas. Somos apenas uma vitrine digital — os negócios são feitos diretamente com os estabelecimentos.

## 🎯 Objetivo

Criar uma plataforma simples, funcional e profissional que demonstre valor real para comércios (mercados, padarias, hortifrutis) e consumidores, servindo como portal de entrada para validação de negócio.

## ✨ Tecnologias Utilizadas

- **Backend**: Python 3 + Flask (API RESTful)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Banco de Dados**: MongoDB Atlas (nuvem)
- **Deploy**: Render.com

## 🚀 Funcionalidades

### Para Consumidores (Página de Ofertas)
- Visualização de produtos com filtro: **"Todos"** ou **"Com Desconto (3 dias)"**
- Busca por nome de produto ou empresa
- Filtro por empresa específica (dropdown)
- Badge **% OFF** automático em produtos com desconto
- Produtos vencidos são ocultados automaticamente (conforme legislação)
- Botão direto para **WhatsApp** do comércio
- Design **mobile-first** (otimizado para celular)

### Para Empresas
- **Painel completo** com acesso via código único gerado pelo admin
- Cadastro simplificado de produtos (validade, preço original, preço com desconto)
- **Edição e exclusão** de produtos cadastrados
- Visualização de produtos vencidos (riscados) para gestão
- Mensagens de status visuais (sucesso/erro)

### Para Administradores
- Cadastro seguro de novas empresas via painel administrativo
- Geração automática de códigos de acesso únicos
- Proteção por senha de admin (via variável de ambiente)
- Busca, ordenação e gestão de empresas cadastradas
- Interface com toast notifications e confirmação inline de exclusão

### Landing Page
- Apresentação do projeto e sua proposta de valor
- Seção "Como Funciona" (3 passos)
- História do projeto (do acadêmico ao serviço real)
- Benefícios para empresas e consumidores

## 🔧 Segurança e Boas Práticas

- ✅ Senha de admin via variável de ambiente (`.env` - nunca vai para o Git)
- ✅ Códigos de acesso únicos por empresa (gerados automaticamente)
- ✅ Validação de permissões (empresa só edita/exclui seus próprios produtos)
- ✅ `.gitignore` configurado para proteger dados sensíveis
- ✅ CORS habilitado para integração segura
- ✅ Produtos vencidos ocultos da visualização pública (conformidade legal)


## 📋 Exemplo de Uso

### Fluxo do Administrador
1. Acesse `/admin.html`
2. Digite a senha de admin
3. Cadastre uma nova empresa (dados: nome, WhatsApp, endereço)
4. O sistema gera um **código único** (ex: `PADARIA-NOVA-ABC123`)
5. Envie o código para a empresa via WhatsApp

### Fluxo da Empresa
1. Acesse `/empresa.html`
2. Digite o código recebido
3. Escolha **"Cadastrar Produto"** → Preencha: nome, validade, preço original, preço com desconto
4. Ou escolha **"Gerenciar Produtos"** → Edite ou exclua itens

### Fluxo do Consumidor
1. Acesse a página inicial `/`
2. Clique em **"Ver Ofertas"**
3. Veja todas as ofertas ou filtre por "Com Desconto (3 dias)"
4. Busque por produto ou empresa
5. Clique no botão do **WhatsApp** para contatar o comércio

## ⚠️ Aviso Importante

> Os produtos devem ser confirmados diretamente no estabelecimento. Os preços podem variar.
> O ValiMarket é apenas uma vitrine digital, não processamos pagamentos.

## 🎨 Design e UX

- **Mobile-first**: 80%+ dos usuários acessarão via celular
- **Cores suaves**: Verde (#38a169) transmite confiança e frescor
- **Cards modernos**: Sombras suaves, bordas arredondadas
- **Navegação intuitiva**: Foco total no botão "Ver Ofertas"
- **Feedback visual**: Toast notifications, mensagens integradas (sem alerts irritantes)
- **Acessibilidade**: Formulários claros, botões com tamanho adequado para toque

## 📈 Status do Projeto

✅ MVP Completo e Funcional  
✅ Landing Page com proposta de valor clara  
✅ MongoDB Atlas integrado  
✅ Deploy configurado no Render  
✅ Filtros inteligentes e % OFF automático  
✅ Painel admin com gestão de empresas  
✅ Estrutura limpa para portfólio  
🚧 Em fase de testes e validação de negócio  


## 📸 Galeria de Screenshots

Aqui estão as capturas de tela do projeto em funcionamento:

<details>
  <summary>🌐 <b>Clique para ver a Tela Inicial</b></summary>
  <br>
  <img src="./assets/01home.png" width="600" alt="Home parte 1"><br><br>
  <img src="./assets/02home.png" width="600" alt="Home parte 2"><br><br>
  <img src="./assets/03home.png" width="600" alt="Home parte 3">
</details>

<details>
  <summary>🏷️ <b>Clique para ver o Painel de Ofertas</b></summary>
  <br>
  <img src="./assets/04ofertas.png" width="600" alt="Painel de Ofertas">
</details>

<details>
  <summary>🏢 <b>Clique para ver o Painel da Empresa</b></summary>
  <br>
  <img src="./assets/05empresa.png" width="600" alt="Empresa parte 1"><br><br>
  <img src="./assets/06empresa.png" width="600" alt="Empresa parte 2"><br><br>
  <img src="./assets/07empresa.png" width="600" alt="Empresa parte 3"><br><br>
  <img src="./assets/08empresa.png" width="600" alt="Empresa parte 4">
</details>
<br>

Veja a galeria completa de telas do sistema na pasta [assets](./assets).


## 🔮 Sobre o Autor

Projeto desenvolvido por **Janderson Duarte**, estudante de Análise e Desenvolvimento de Sistemas.

O ValiMarket nasceu como um projeto acadêmico, mas percebi seu potencial real: reduzir o desperdício de alimentos no varejo enquanto gera economia para consumidores. Hoje o projeto é um MVP em crescimento, com planos de expansão.

- **GitHub**: [jandersonhp](https://github.com/jandersonhp)
- **LinkedIn**: [jandersonduarteabr](https://www.linkedin.com/in/jandersonduarteabr/)
- **Email**: jandersonduarte@yahoo.com.br

---

**Contato**: jandersonduarte@yahoo.com.br
