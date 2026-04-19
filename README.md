

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

# 2. Instale as dependências (recomendado uv)
uv sync

# 3. Configure as credenciais
cp .env.example .env
# Edite o .env com suas chaves das clouds

# 4. Rode o MCP Server
uv run src/ai_multicloud_agent/main.py run