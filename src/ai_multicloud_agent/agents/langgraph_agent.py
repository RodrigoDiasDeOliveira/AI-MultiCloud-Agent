# src/ai_multicloud_agent/agents/langgraph_agent.py

from typing import Annotated, Sequence, TypedDict
import operator
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_openai import ChatOpenAI
import structlog
from rich.console import Console

from ai_multicloud_agent.mcp.client import MCPToolWrapper

console = Console()
logger = structlog.get_logger()

# Estado do agente
class AgentState(TypedDict):
    messages: Annotated[Sequence, operator.add]
    sender: str

# Wrapper que transforma todas as tools do MCP em ferramentas do LangChain
mcp_wrapper = MCPToolWrapper()

# LLM principal (pode trocar por Grok, Claude, etc.)
llm = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = llm.bind_tools(mcp_wrapper.get_all_tools())

def agent_node(state: AgentState):
    """Nó principal: decide qual tool chamar ou responder diretamente."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    
    logger.info("agent_decision", tool_calls=len(response.tool_calls) if hasattr(response, 'tool_calls') else 0)
    return {"messages": [response], "sender": "agent"}

def should_continue(state: AgentState):
    """Decide se deve chamar tools ou finalizar."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Construção do Grafo
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(mcp_wrapper.get_all_tools()))

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", END: END}
)
workflow.add_edge("tools", "agent")

# Compila o agente
multi_cloud_graph = workflow.compile()


# ====================== Funções de uso ======================

async def run_intelligent_agent(query: str, verbose: bool = True) -> str:
    """Executa o agente LangGraph com integração real ao MCP."""
    if verbose:
        console.print(f"\n[bold cyan]👤 Pergunta:[/bold cyan] {query}")

    inputs = {"messages": [HumanMessage(content=query)]}
    
    try:
        result = multi_cloud_graph.invoke(inputs)
        final_message = result["messages"][-1]
        
        response = final_message.content
        
        if verbose:
            console.print(f"[bold green]🤖 MultiCloud Agent:[/bold green] {response}")
        
        return response
        
    except Exception as e:
        logger.error("langgraph_error", error=str(e))
        error_msg = f"Erro ao processar sua solicitação: {str(e)}"
        if verbose:
            console.print(f"[red]{error_msg}[/red]")
        return error_msg


# Para teste rápido
if __name__ == "__main__":
    import asyncio
    asyncio.run(run_intelligent_agent("Crie um bucket S3 chamado meus-backups na região us-east-1"))