import streamlit as st
import anthropic
import openai
from typing import Generator

# Page configuration
st.set_page_config(
    page_title="F5 LLM Inference",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clean design
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput > div > div > input {
        border-radius: 10px;
    }
    .stButton > button {
        border-radius: 10px;
        background-color: #e40046;
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.5rem 2rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #c4003d;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
    }
    .assistant-message {
        background-color: #f0f0f0;
        border-left: 4px solid #e40046;
    }
    .f5-logo {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        color: #e40046;
        margin: 2rem 0;
        font-family: 'Arial', sans-serif;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
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

# F5 Logo
st.markdown('<div class="f5-logo">F5</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">LLM Inference Platform</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Provider selection
    provider = st.selectbox(
        "LLM Provider",
        ["Anthropic", "OpenAI"],
        key="provider_select"
    )
    st.session_state.provider = provider

    # API Key input
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
    else:  # OpenAI
        model = st.selectbox(
            "Model",
            [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo"
            ]
        )

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

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("### About")
    st.markdown("""
    This app provides a unified interface for interacting with various LLM providers.

    **Supported Providers:**
    - Anthropic (Claude)
    - OpenAI (GPT)
    """)

# Main chat interface
st.markdown("---")

# Display chat history
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]

    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>',
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong><br>{content}</div>',
                   unsafe_allow_html=True)

# Chat input
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
        return f"Error: {str(e)}"

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
        return f"Error: {str(e)}"

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    if not st.session_state.api_key:
        st.error("⚠️ Please enter your API key in the sidebar.")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response from selected provider
        with st.spinner("Thinking..."):
            if st.session_state.provider == "Anthropic":
                response = get_anthropic_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )
            else:  # OpenAI
                response = get_openai_response(
                    st.session_state.messages,
                    model,
                    temperature,
                    max_tokens
                )

        # Add assistant response to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Rerun to update chat display
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #999; font-size: 0.9rem;">Powered by F5 | Streamlit LLM Inference Platform</p>',
    unsafe_allow_html=True
)
