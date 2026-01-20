import streamlit as st
from utils import get_translation, get_summary

# Page Configuration
st.set_page_config(
    page_title="AI Foundry - Tradução & Sumarização",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        color: #333333;
    }
    .stButton>button {
        background-color: #0078D4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #005a9e;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌐 AI Sum: Tradução & Sumarização Multilíngue")
st.markdown("### Desenvolvido com Serviços de IA do Azure")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.subheader("Idioma de Origem")
    source_language = st.selectbox(
        "Selecione o idioma do texto original",
        options=["en", "pt"],
        format_func=lambda x: {
            "en": "Inglês",
            "pt": "Português"
        }.get(x, x),
        help="O idioma em que o texto de entrada está escrito."
    )
    
    st.subheader("Opções de Tradução")
    target_language = st.selectbox(
        "Selecione o Idioma de Destino",
        options=["en", "pt", "es", "fr", "de", "it", "ja", "zh-Hans"],
        format_func=lambda x: {
            "en": "Inglês",
            "pt": "Português",
            "es": "Espanhol",
            "fr": "Francês",
            "de": "Alemão",
            "it": "Italiano",
            "ja": "Japonês",
            "zh-Hans": "Chinês (Simplificado)"
        }.get(x, x)
    )
    
    st.subheader("Opções de Sumarização")
    summary_type = st.radio(
        "Selecione o Tipo de Resumo",
        options=["Extractive", "Abstractive"],
        format_func=lambda x: "Extrativo" if x == "Extractive" else "Abstrativo",
        help="Extrativo: Seleciona frases-chave do texto original.\nAbstrativo: Gera um novo resumo com suas próprias palavras."
    )

# Main Content
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Texto de Entrada")
    input_text = st.text_area("Digite o texto para processar:", height=300, placeholder="Digite ou cole seu texto aqui...")

with col2:
    st.subheader("📤 Saída")
    output_placeholder = st.empty()
    
    if not input_text:
        output_placeholder.info("Por favor, digite um texto na caixa de entrada para ver os resultados.")

# Action Buttons
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("🔤 Traduzir Texto"):
        if input_text:
            with st.spinner("Traduzindo..."):
                translation_result = get_translation(input_text, target_language, source_language)
                output_placeholder.success("Tradução Concluída!")
                st.session_state['result'] = translation_result
                st.session_state['result_type'] = "Tradução"
        else:
            st.warning("Por favor, digite algum texto primeiro.")

with col_btn2:
    if st.button("📄 Sumarizar Texto"):
        if input_text:
            with st.spinner("Sumarizando..."):
                summary_result = get_summary(input_text, summary_type)
                output_placeholder.success("Sumarização Concluída!")
                st.session_state['result'] = summary_result
                st.session_state['result_type'] = f"Resumo ({'Extrativo' if summary_type == 'Extractive' else 'Abstrativo'})"
        else:
            st.warning("Por favor, digite algum texto primeiro.")

# Display Result if exists
if 'result' in st.session_state and input_text:
    with col2:
        output_placeholder.markdown(f"**{st.session_state.get('result_type', 'Resultado')}:**")
        st.text_area("Resultado:", value=st.session_state['result'], height=250, key="result_area")

# Footer
st.markdown("---")
st.markdown("Desenvolvido por Guilherme Pereira")
