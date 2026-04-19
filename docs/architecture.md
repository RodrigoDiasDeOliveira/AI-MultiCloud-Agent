# Arquitetura AI MultiCloud Agent

Este documento descreve a arquitetura inicial do agente que unifica operações em múltiplas nuvens.

- `src/ai_multicloud_agent/main.py`: ponto de entrada do servidor MCP.
- `src/ai_multicloud_agent/config`: definições de configuração e credenciais com Pydantic.
- `src/ai_multicloud_agent/mcp`: servidor MCP e registro de ferramentas.
- `src/ai_multicloud_agent/tools`: ferramentas de automação divididas por domínio e provedor.
- `src/ai_multicloud_agent/providers`: factory e adaptadores de provedores de nuvem.
- `src/ai_multicloud_agent/agents`: agentes conversacionais de alto nível.
- `src/ai_multicloud_agent/utils`: utilitários e validações comuns.
