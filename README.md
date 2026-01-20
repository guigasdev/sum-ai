# 🌐 AI Foundry - Tradução & Sumarização Multilíngue

Este é um aplicativo web profissional desenvolvido com **Streamlit** que utiliza o poder do **Microsoft Azure AI Foundry** para realizar traduções de alta qualidade e sumarização inteligente de textos (extrativa e abstrativa).

## 🏗️ Arquitetura da Solução

O diagrama abaixo ilustra o fluxo de dados e a integração entre o frontend (Streamlit) e os serviços cognitivos do Azure (Backend).

```mermaid
graph TD
    User["👤 Usuário"] -->|Interage via Navegador| UI["💻 Interface Streamlit (Frontend)"]
    
    subgraph "Aplicação Python"
        UI -->|Envia Texto e Configurações| Utils["⚙️ Módulo Backend (utils.py)"]
        Utils -->|Lê Credenciais| Env["🔐 Variáveis de Ambiente (.env)"]
    end
    
    subgraph "Azure AI Foundry (Nuvem)"
        Utils -->|Requisição REST/SDK| Translator["🔤 Azure AI Translator"]
        Utils -->|Requisição REST/SDK| Language["🧠 Azure AI Language Service"]
    end
    
    Translator -->|Retorna Texto Traduzido| Utils
    Language -->|Retorna Resumo (Extrativo/Abstrativo)| Utils
    Utils -->|Processa e Formata| UI
    UI -->|Exibe Resultado| User
```

## ✨ Funcionalidades

### 1. 🔤 Tradução Multilíngue
Traduza textos entre diversos idiomas com alta precisão.
- **Entrada:** Suporte explícito para Inglês e Português.
- **Saída:** Inglês, Português, Espanhol, Francês, Alemão, Italiano, Japonês e Chinês (Simplificado).

### 2. 📝 Sumarização de Texto
Utiliza modelos avançados de linguagem para resumir textos longos de duas formas:
- **Resumo Extrativo:** Identifica e extrai as frases mais importantes do texto original, mantendo a redação exata. Ideal para pinçar pontos-chave.
- **Resumo Abstrativo:** Gera um novo texto, reescrito com as próprias palavras da IA, capturando a essência do conteúdo de forma concisa.

## 🚀 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/):** Framework para criação rápida de web apps de dados em Python.
- **[Azure AI Translator](https://azure.microsoft.com/en-us/products/ai-services/translator):** Serviço de tradução neural em tempo real.
- **[Azure AI Language Service](https://azure.microsoft.com/en-us/products/ai-services/language-service):** Serviço para análise de texto, incluindo sumarização.
- **Python 3.9+:** Linguagem base do projeto.
- **Azure SDK for Python:** Bibliotecas oficiais (`azure-ai-translation-text`, `azure-ai-textanalytics`).

## 🛠️ Pré-requisitos

1.  **Python 3.9 ou superior** instalado.
2.  Uma conta no **Microsoft Azure**.
3.  Recursos criados no Azure:
    *   **Translator** (para obter a chave e região).
    *   **Language Service** (para obter a chave e endpoint).

## 📦 Instalação e Configuração Local

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/ai-foundry-translate-sum.git
    cd ai-foundry-translate-sum
    ```

2.  **Crie um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto (baseado no exemplo abaixo) e preencha com suas chaves do Azure:

    ```env
    # Azure Translator
    AZURE_TRANSLATOR_KEY=sua_chave_aqui
    AZURE_TRANSLATOR_REGION=sua_regiao_aqui (ex: eastus)
    AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com/

    # Azure AI Language Service
    AZURE_LANGUAGE_KEY=sua_chave_aqui
    AZURE_LANGUAGE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
    ```

5.  **Execute a aplicação:**
    ```bash
    streamlit run main.py
    ```

## ☁️ Guia de Deploy (Implantação)

### Opção 1: Azure App Service (Recomendado para Produção)
O projeto já inclui o arquivo `startup.sh` necessário para deploy no Azure Web Apps for Containers (Linux).

1.  Crie um **Web App** no Azure Portal (Python 3.9+, Linux).
2.  Em **Configuration** -> **General settings**, defina o "Startup Command" como:
    ```bash
    sh startup.sh
    ```
3.  Em **Environment variables**, adicione todas as chaves do seu arquivo `.env`.
4.  Faça o deploy do código via VS Code (Azure Extension) ou GitHub Actions.

### Opção 2: Streamlit Community Cloud (Rápido e Gratuito)
1.  Suba o código para um repositório GitHub.
2.  Conecte-se ao [share.streamlit.io](https://share.streamlit.io).
3.  Ao criar o app, vá em **Advanced Settings** e adicione suas chaves no formato TOML na seção "Secrets":
    ```toml
    AZURE_TRANSLATOR_KEY = "sua_chave"
    AZURE_TRANSLATOR_REGION = "brazilsouth"
    ...
    ```

## 📂 Estrutura de Arquivos

```
.
├── main.py             # Frontend da aplicação (Interface Streamlit)
├── utils.py            # Lógica de Backend (Integração com Azure SDKs)
├── requirements.txt    # Lista de dependências Python
├── .env                # Arquivo de configuração (NÃO COMITAR)
├── startup.sh          # Script de inicialização para deploy no Azure
└── README.md           # Documentação do projeto
```

---
**Autor:** Desenvolvido como parte do projeto de integração com AI Foundry por Guilherme.
