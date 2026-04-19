

# AI-MultiCloud-Agent

**MCP Server completo para gerenciamento multi-cloud com AI Agents**

Projeto moderno (2026) que expõe um **Model Context Protocol (MCP) Server** permitindo que agentes de IA controlem infraestrutura completa em **AWS, Azure, Google Cloud e Oracle OCI** usando linguagem natural.

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

## 🚀 Como rodar

```bash
# 1. Clone o repositório
git clone https://github.com/seuusuario/ai-multicloud-agent.git
cd ai-multicloud-agent

# 2. Instale as dependências do projeto e de desenvolvimento
uv sync --all-groups

# 3. Configure as credenciais
cp .env.example .env
# Edite o .env com suas chaves das clouds

# 4. Execute o MCP Server
python src/ai_multicloud_agent/main.py run
```

## 🧪 Testes

```bash
# Execute a suíte de testes
pytest -q
```

## 🔧 Health endpoint

O projeto exporta um app FastAPI em `src/ai_multicloud_agent/main.py` para testes. Ele expõe a rota:

- `GET /health`

Esse endpoint é usado pelos testes unitários e de integração.

## 📌 Observações

- O pacote usa layout `src/`.
- Para desenvolvimento, use `uv sync --all-groups` para garantir instalação das dependências de teste e desenvolvimento.
- O servidor principal roda como CLI Typer, mas a aplicação FastAPI também está disponível para verificação de saúde e compatibilidade de testes.
