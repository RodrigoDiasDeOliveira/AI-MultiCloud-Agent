

# AI-MultiCloud-Agent

**MCP Server completo para gerenciamento multi-cloud com AI Agents**

Projeto moderno (2026) que expõe um **Model Context Protocol (MCP) Server** permitindo que agentes de IA controlem infraestrutura completa em **AWS, Azure, Google Cloud e Oracle OCI** usando linguagem natural.

**Status:** ✅ Totalmente funcional e pronto para uso pessoal e corporativo.

## ✨ Funcionalidades

- Suporte completo a múltiplas nuvens (AWS + Azure + GCP + Oracle OCI)
- Categorias de ferramentas:
  - **Compute** (VMs, scaling, instances)
  - **Storage** (Object, Block, File)
  - **Database** (RDS, Cosmos DB, Cloud SQL, Autonomous DB)
  - **Networking** (VPC, Load Balancers, Firewalls, CDN)
  - **IAM** (Roles, Policies, Users)
  - **Serverless** (Lambda, Azure Functions, Cloud Functions)
  - **Containers** (ECS, AKS, GKE, OKE)
  - **Monitoring & Logging**
  - **Security** (KMS, Key Vault, WAF, Certificates)
- Padrão **search-and-execute** nativo do MCP
- Auto-discovery de tools
- Logging estruturado + segurança
- Pronto para Docker e produção

## 🚀 Como Instalar e Rodar

### 1. Clone e Configure o Ambiente

```bash
# Clone o repositório
git clone https://github.com/seuusuario/ai-multicloud-agent.git
cd ai-multicloud-agent

# Crie um arquivo .env com suas credenciais
cp .env.example .env
# Edite o .env com suas chaves das clouds (veja seção de Credenciais abaixo)
```

### 2. Instale Dependências Base

```bash
# Instalação básica (only MCP Server)
pip install -e .

# OU com dependências de desenvolvimento
pip install -e ".[dev]"
```

### 3. Instale Dependências de Cloud (Opcional)

Instale apenas os provedores de nuvem que você planeja usar:

```bash
# AWS
pip install -e ".[aws]"

# Azure
pip install -e ".[azure]"

# Google Cloud
pip install -e ".[gcp]"

# Oracle OCI
pip install -e ".[oci]"

# Todas as nuvens
pip install -e ".[aws,azure,gcp,oci]"

# Com segurança via keyring
pip install -e ".[security]"

# Frontend Streamlit
pip install -e ".[frontend]"
```

### 4. Configure as Credenciais

Edite o arquivo `.env` com suas credenciais:

```bash
# Abra e edite o arquivo
nano .env
# (ou use seu editor preferido)
```

**Credenciais por Provedor:**

#### AWS
```env
AWS__ACCESS_KEY_ID=AKIA5YOURKEY
AWS__SECRET_ACCESS_KEY=your-secret-key
AWS__REGION=us-east-1
```
Ou use `~/.aws/credentials` deixando estas linhas vazias.

#### Azure
```env
AZURE__TENANT_ID=your-tenant-id
AZURE__CLIENT_ID=your-client-id
AZURE__CLIENT_SECRET=your-client-secret
AZURE__SUBSCRIPTION_ID=your-subscription-id
```

#### Google Cloud
```env
GCP__PROJECT_ID=your-project-id
GCP__CREDENTIALS_PATH=~/.gcp/service-account-key.json
```

#### Oracle OCI
```env
ORAC LE__CONFIG_FILE=~/.oci/config
ORAC LE__PROFILE=DEFAULT
ORAC LE__NAMESPACE=your-namespace
ORAC LE__COMPARTMENT_ID=your-compartment-id
```

### 5. Inicie o Server MCP

```bash
# Iniciar na porta padrão (8000)
ai-multicloud-agent run

# Com opções personalizadas
ai-multicloud-agent run --host 0.0.0.0 --port 3000 --verbose

# Listar todas as tools disponíveis
ai-multicloud-agent tools

# Filtrar tools por categoria
ai-multicloud-agent tools compute
ai-multicloud-agent tools storage
ai-multicloud-agent tools database

# Ver versão
ai-multicloud-agent version
```

## 🧪 Testes

```bash
# Execute a suíte de testes completa
ai-multicloud-agent run  # Valida estrutura geral

# Com pytest
pip install -e ".[dev]"
pytest -v
pytest -q  # modo silencioso
```

## 🔌 API FastAPI (Health Check)

O projeto exporta uma aplicação FastAPI para testes e health checks:

```python
from ai_multicloud_agent.main import app
```

**Endpoints Disponíveis:**

- `GET /health` — Status geral do servidor
- `GET /health/providers` — Status de cada cloud provider
- `GET /tools` — Descoberta automática de tools

**Exemplo:**
```bash
# Executar apenas a API FastAPI
python -c "from ai_multicloud_agent.main import app; print(app.routes)"
```

## 🐳 Docker

```bash
# Build da imagem
docker build -t ai-multicloud-agent:latest .

# Executar com credenciais via env vars
docker run -e AWS__ACCESS_KEY_ID=your-key \
           -e AWS__SECRET_ACCESS_KEY=your-secret \
           -p 8000:8000 ai-multicloud-agent:latest
```

## 📦 Estrutura do Projeto

```
ai-multicloud-agent/
├── src/ai_multicloud_agent/
│   ├── main.py                 # CLI Typer + FastAPI app
│   ├── config/settings.py      # Configuração via pydantic
│   ├── core/                   # Abstrações base (providers, registry)
│   ├── providers/              # Factory e adapters (AWS, Azure, GCP, OCI)
│   ├── tools/                  # Ferramentas por categoria
│   │   ├── compute/
│   │   ├── storage/
│   │   ├── database/
│   │   ├── networking/
│   │   ├── iam/
│   │   └── ...
│   ├── mcp/                    # Servidor MCP via fastmcp
│   └── utils/                  # Logging, segurança, helper
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
│   └── architecture.md
└── pyproject.toml              # Dependências e metadata
```

## 🔐 Segurança

- Credenciais **nunca** são logadas
- Suporte a `keyring` para armazenamento seguro (opção `resolve_secret`)
- Use `.env` local (não versionado) para credenciais
- Em produção, use variáveis de ambiente ou secrets do seu orchestrator

## 📌 Notas Importantes

- O pacote usa layout `src/` seguindo PEP 420
- Ferramentas são auto-descobertas via `pkgutil`
- Azure/GCP com dependências parciais serão ignoradas se libs não estiverem instaladas
- Use `LOG_LEVEL=DEBUG` no `.env` para troubleshooting
- Compatível com Python 3.11+

## 🤝 Contribuindo

Para adicionar novas tools:

1. Crie um arquivo em `src/ai_multicloud_agent/tools/{categoria}/{provider}.py`
2. Use o decorator `@tool` do fastmcp
3. Implemente funções com docstrings claras
4. As tools são auto-registradas na inicialização
