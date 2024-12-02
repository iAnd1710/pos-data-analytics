import streamlit as st
from components import analysis, history, predictions, about

# Configurações iniciais
def setup():
    st.set_page_config(
        page_title="Dashboard de Preços do Petróleo",
        page_icon="🛢️",
    )

# Função principal
def main():
    setup()
    st.sidebar.image("assets/logo.jpg", width=150)
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para", ("Análise de Dados", "Histórico", "Previsões", "Sobre"))

    if page == "Análise de Dados":
        analysis.show_analysis()
    elif page == "Histórico":
        history.show_history()
    elif page == "Previsões":
        predictions.show_predictions_page()
    elif page == "Sobre":
        about.show_about()

if __name__ == "__main__":
    main()
