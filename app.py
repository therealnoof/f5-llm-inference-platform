import streamlit as st
import anthropic
import openai
import requests

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, modern design
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        max-width: 1200px;
    }
    div[data-testid="stSidebarNav"] {
        padding-top: 0;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    h1 {
        color: #1f1f1f;
        font-weight: 600;
        padding-bottom: 0.5rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stButton > button {
        border-radius: 0.5rem;
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: 500;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #ff3333;
        box-shadow: 0 2px 8px rgba(255, 75, 75, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "provider" not in st.session_state:
    st.session_state.provider = "Anthropic"
if "local_host" not in st.session_state:
    st.session_state.local_host = "127.0.0.1"
if "local_port" not in st.session_state:
    st.session_state.local_port = 1337

# Header
st.title("💬 AI Assistant")
st.caption("Chat with Claude, GPT, or Local models")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    st.divider()

    # Provider selection
    provider = st.selectbox(
        "LLM Provider",
        ["Anthropic", "OpenAI", "Local"],
        key="provider_select"
    )
    st.session_state.provider = provider

    # Local server configuration
    if provider == "Local":
        st.info("💡 Connect to a local API server (e.g., LM Studio, Ollama, vLLM)")

        col1, col2 = st.columns([2, 1])
        with col1:
            local_host = st.text_input(
                "Host",
                value=st.session_state.local_host,
                help="Local server host address"
            )
            st.session_state.local_host = local_host

        with col2:
            local_port = st.number_input(
                "Port",
                min_value=1,
                max_value=65535,
                value=st.session_state.local_port,
                help="Local server port"
            )
            st.session_state.local_port = local_port

        # Show the full URL
        local_url = f"http://{local_host}:{local_port}"
        st.caption(f"🌐 Server URL: `{local_url}`")

    # API Key input
    if provider == "Local":
        api_key = st.text_input(
            "API Key (Optional)",
            type="password",
            value=st.session_state.api_key,
            help="Some local servers require an API key"
        )
    else:
        api_key = st.text_input(
            "API Key",
            type="password",
            value=st.session_state.api_key,
            help=f"Enter your {provider} API key"
        )
    st.session_state.api_key = api_key

    # Model selection based on provider
    if provider == "Anthropic":
        model = st.selectbox(
            "Model",
            [
                "claude-sonnet-4-5-20250929",
                "claude-3-5-sonnet-20241022",
                "claude-3-5-haiku-20241022",
                "claude-3-opus-20240229"
            ]
        )
    elif provider == "OpenAI":
        model = st.selectbox(
            "Model",
            [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ]
        )
    else:  # Local
        model = st.text_input(
            "Model Name",
            value="local-model",
            help="Enter the model name from your local server"
        )

    st.divider()

    # Advanced settings
    with st.expander("⚡ Advanced Settings"):
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Controls randomness in responses"
        )

        # Max tokens
        max_tokens = st.slider(
            "Max Tokens",
            min_value=256,
            max_value=4096,
            value=1024,
            step=256,
            help="Maximum length of the response"
        )

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    # About section
    st.markdown("### About")
    st.markdown("""
    A simple interface for interacting with LLM providers.

    **Supported:**
    - 🤖 Anthropic Claude
    - 🔮 OpenAI GPT
    - 🖥️ Local API Servers
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input functions
def get_anthropic_response(messages: list, model: str, temperature: float, max_tokens: int) -> str:
    """Get response from Anthropic API"""
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)

        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            anthropic_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=anthropic_messages
        )

        return response.content[0].text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_openai_response(messages: list, model: str, temperature: float, max_tokens: int) -> str:
    """Get response from OpenAI API"""
    try:
        client = openai.OpenAI(api_key=st.session_state.api_key)

        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            openai_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        response = client.chat.completions.create(
            model=model,
            messages=openai_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_local_response(messages: list, model: str, temperature: float, max_tokens: int) -> str:
    """Get response from Local API Server (OpenAI-compatible)"""
    try:
        # Build the local server URL
        base_url = f"http://{st.session_state.local_host}:{st.session_state.local_port}"

        # Convert messages to OpenAI format
        api_messages = []
        for msg in messages:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Prepare the request
        headers = {
            "Content-Type": "application/json"
        }

        # Add API key if provided
        if st.session_state.api_key:
            headers["Authorization"] = f"Bearer {st.session_state.api_key}"

        payload = {
            "model": model,
            "messages": api_messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Make the request to local server
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            return data["choices"][0]["message"]["content"]
        else:
            return f"❌ Error: Server returned {response.status_code} - {response.text}"

    except requests.exceptions.ConnectionError:
        return f"❌ Connection Error: Could not connect to {base_url}. Make sure your local server is running."
    except requests.exceptions.Timeout:
        return "❌ Timeout Error: The request took too long. Try again or check your server."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# User input
if prompt := st.chat_input("What would you like to know?"):
    # Validation
    if provider == "Local":
        if not st.session_state.local_host or not st.session_state.local_port:
            st.error("⚠️ Please configure your local server host and port in the sidebar.")
            st.stop()
    else:
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your API key in the sidebar.")
            st.stop()

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.provider == "Anthropic":
                response = get_anthropic_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )
            elif st.session_state.provider == "OpenAI":
                response = get_openai_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )
            else:  # Local
                response = get_local_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )

        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Rerun to update the interface
    st.rerun()
