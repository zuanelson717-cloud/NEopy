# 🍺 Sistema de Gerenciamento de Faturas - Loja de Bebidas

Um sistema web completo para login, cadastro e gerenciamento de faturas online para lojas de bebidas. Desenvolvido com Python Flask, SQLite, HTML5, CSS3 e JavaScript.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Tecnologias](#tecnologias)
- [API Endpoints](#api-endpoints)
- [Segurança](#segurança)
- [Melhorias Futuras](#melhorias-futuras)

## ✨ Funcionalidades

### Autenticação
- ✅ Cadastro de novos usuários
- ✅ Login com autenticação segura (hash de senha)
- ✅ Logout seguro
- ✅ Proteção de rotas (login_required)

### Gerenciamento de Perfil
- ✅ Visualizar informações do perfil
- ✅ Atualizar dados pessoais
- ✅ Visualizar data de cadastro
- ✅ Informações da empresa

### Gerenciamento de Faturas
- ✅ Criar novas faturas
- ✅ Visualizar lista de faturas
- ✅ Ver detalhes completos da fatura
- ✅ Acompanhar status (Pendente/Pago)
- ✅ Marcar fatura como paga
- ✅ Imprimir faturas

### Dashboard
- ✅ Estatísticas de faturas
- ✅ Total de faturas cadastradas
- ✅ Valor total de faturas
- ✅ Valor pendente
- ✅ Tabela com histórico de faturas

## 🔧 Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

## 📥 Instalação

### 1. Clone ou Baixe o Repositório

```bash
git clone https://github.com/zuanelson717-cloud/Neopy.git
cd Neopy/beverage_system
```

### 2. Crie um Ambiente Virtual (Opcional, mas Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação

```bash
python app.py
```

### 5. Acesse no Navegador

Abra seu navegador e acesse: **http://localhost:5000**

## 🚀 Como Usar

### 1. Primeira Visita - Criar Conta

1. Clique em "Criar uma conta" na página de login
2. Preencha os dados obrigatórios:
   - Nome Completo
   - Usuário
   - Email
   - Senha
3. Preenchimento opcional:
   - Nome da Empresa
   - Telefone
4. Clique em "Registrar"
5. Você será redirecionado para o login

### 2. Fazer Login

1. Digite seu usuário e senha
2. Clique em "Entrar"
3. Você será direcionado ao Dashboard

### 3. Usar o Dashboard

**Visualizar Estatísticas:**
- Veja o total de faturas, valor total e pendências em cards de resumo

**Gerenciar Faturas:**
- Veja todas as suas faturas na tabela
- Clique em "Visualizar" para ver detalhes completos
- Clique em "+ Nova Fatura" para criar uma nova

### 4. Criar Nova Fatura

1. Clique em "+ Nova Fatura" no Dashboard
2. Preencha:
   - Nº Fatura (identificador único)
   - Valor Total
   - Descrição
3. Clique em "Criar Fatura"

### 5. Visualizar Detalhes da Fatura

- Veja informações da empresa
- Acompanhe status (Pendente/Pago)
- Imprima a fatura
- Baixe em PDF (recurso em desenvolvimento)
- Marque como pago

### 6. Atualizar Perfil

1. Clique em "Perfil" na barra de navegação
2. Atualize suas informações
3. Clique em "Salvar Alterações"

## 📁 Estrutura do Projeto

```
beverage_system/
├── app.py                    # Aplicação Flask principal
├── requirements.txt          # Dependências do projeto
├── beverage_store.db         # Banco de dados SQLite (gerado automaticamente)
├── templates/
│   ├── base.html            # Template base (navbar, footer)
│   ├── login.html           # Página de login
│   ├── register.html        # Página de registro
│   ├── dashboard.html       # Dashboard principal
│   ├── profile.html         # Página de perfil
│   └── invoice_detail.html  # Detalhes da fatura
└── static/
    ├── css/
    │   └── style.css        # Estilos CSS completos
    └── js/
        └── script.js        # JavaScript auxiliar
```

## 🛠️ Tecnologias

### Backend
- **Flask** - Framework web Python
- **SQLite** - Banco de dados
- **Werkzeug** - Utilitários de segurança (hash de senha)

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilos responsivos
- **JavaScript** - Interatividade
- **Fetch API** - Requisições assíncronas

## 🔌 API Endpoints

### Autenticação
- `GET /` - Redirecionamento (login ou dashboard)
- `GET/POST /login` - Login de usuário
- `GET/POST /register` - Registro de novo usuário
- `GET /logout` - Logout do usuário

### Perfil
- `GET /profile` - Visualizar perfil
- `POST /profile/update` - Atualizar perfil

### Dashboard
- `GET /dashboard` - Dashboard principal

### Faturas
- `GET /invoice/<id>` - Visualizar detalhes da fatura
- `POST /api/invoices` - Criar nova fatura
- `PUT /api/invoices/<id>/status` - Atualizar status da fatura

## 🔐 Segurança

✅ **Implementado:**
- Senhas criptografadas com Werkzeug (PBKDF2)
- Proteção de rotas com login_required
- Session management seguro
- Validação de entrada de dados
- SQL com prepared statements (proteção contra SQL injection)

⚠️ **Recomendações para Produção:**
- Mude `SECRET_KEY` em `app.py`
- Use um servidor WSGI (Gunicorn, uWSGI)
- Configure HTTPS/SSL
- Use banco de dados PostgreSQL ou MySQL
- Implemente CSRF protection
- Configure rate limiting
- Use variáveis de ambiente para dados sensíveis

## 🚀 Melhorias Futuras

- [ ] Exportar faturas em PDF
- [ ] Envio de faturas por email
- [ ] Gráficos de análise financeira
- [ ] Pagamento online integrado
- [ ] Notificações por email
- [ ] Relatórios personalizados
- [ ] Integração com APIs de pagamento
- [ ] Autenticação com 2FA
- [ ] Sistema de permissões (admin, cliente, etc)
- [ ] App mobile

## 📝 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 👨‍💻 Desenvolvedor

Desenvolvido por: **zuanelson717-cloud**
Data: 2026

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

**Aproveite o Sistema! 🎉**
