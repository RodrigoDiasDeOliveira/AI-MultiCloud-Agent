import streamlit as st


def main() -> None:
    st.set_page_config(
        page_title="AI MultiCloud Agent",
        page_icon="🚀",
        layout="wide",
    )

    st.title("AI MultiCloud Agent")
    st.markdown(
        "Uma interface simples para visualizar e testar ferramentas MCP de multi-cloud."
    )

    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Seção", ["Dashboard", "Tools", "Status", "Logs"])

    if page == "Dashboard":
        st.header("Dashboard")
        st.markdown(
            "Use esta interface para inspecionar o catálogo de ferramentas e planejar execuções de cloud."
        )
        st.info("Ainda não há integração direta ao servidor MCP nesta versão inicial.")

    if page == "Tools":
        st.header("Catálogo de Tools")
        st.markdown(
            "As ferramentas são carregadas a partir de `src/ai_multicloud_agent/tools` e expostas pelo servidor MCP."
        )
        st.write(
            {
                "Compute": [
                    "aws_list_instances",
                    "aws_create_ec2",
                    "aws_stop_instance",
                ],
                "Storage": ["aws_create_s3_bucket", "aws_list_buckets"],
                "IAM": ["aws_list_roles", "aws_get_policy"],
            }
        )

    if page == "Status":
        st.header("Status do Sistema")
        st.markdown("Conexão com clouds, status do servidor e indicadores de credenciais.")
        st.warning("O backend ainda não expõe um endpoint direto de status nesta versão inicial.")

    if page == "Logs":
        st.header("Logs")
        st.markdown("Os logs do servidor são gerenciados através da configuração de logging no backend.")
        st.text("Nenhum log disponível localmente nesta versão inicial.")


if __name__ == "__main__":
    main()
