#!/bin/bash
# scripts/run_agent.sh

echo "🚀 Iniciando AI-MultiCloud-Agent + LangGraph Agent"

# Inicia o MCP Server em background
echo "📡 Iniciando MCP Server..."
uv run src/ai_multicloud_agent/main.py run --host 0.0.0.0 --port 8000 &

SERVER_PID=$!
sleep 3  # Aguarda o servidor iniciar

# Inicia o agente inteligente
echo "🤖 Iniciando Agente LangGraph..."
uv run -m ai_multicloud_agent.agents.langgraph_agent

# Finaliza o servidor ao encerrar
kill $SERVER_PID 2>/dev/null"$APP_HOST" --port "$APP_PORT" --reload
