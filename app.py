import streamlit as st
import anthropic
import openai
import requests
import json
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Coffee Shop AI Assistant",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File-based persistence
SETTINGS_FILE = Path.home() / ".coffee_ai_settings.json"

def load_settings():
    """Load settings from file"""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading settings: {e}")
    return {}

def save_settings(settings):
    """Save settings to file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        st.error(f"Error saving settings: {e}")

def clear_settings():
    """Clear saved settings file"""
    try:
        if SETTINGS_FILE.exists():
            SETTINGS_FILE.unlink()
        return True
    except Exception as e:
        st.error(f"Error clearing settings: {e}")
        return False

def save_current_settings():
    """Save current session state to settings file"""
    settings = {
        "provider": st.session_state.provider,
        "api_key": st.session_state.api_key,
        "model": st.session_state.model,
        "local_host": st.session_state.local_host,
        "local_port": st.session_state.local_port,
        "enable_guardrails": st.session_state.enable_guardrails,
        "calypso_api_key": st.session_state.calypso_api_key,
        "temperature": st.session_state.temperature,
        "max_tokens": st.session_state.max_tokens
    }
    save_settings(settings)

# Custom CSS for cozy coffee shop theme with fall colors
st.markdown("""
<style>
    /* Main background - cream color */
    .main {
        background-color: #faf7f2;
        background-image:
            linear-gradient(rgba(212, 137, 90, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 137, 90, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
        color: #000000;
    }

    /* Ensure all text is black */
    p, div, span, label, li, td, th {
        color: #000000 !important;
    }

    .stApp {
        background-color: #faf7f2;
    }

    /* Center chat content */
    .main .block-container {
        max-width: 900px;
        padding-left: 5rem;
        padding-right: 5rem;
        padding-bottom: 8rem;
        padding-top: 2rem;
        margin: 0 auto;
    }

    /* Move chat messages up */
    .main {
        padding-bottom: 0 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f5f0e8;
        border-right: 2px solid #d4895a;
    }

    [data-testid="stSidebar"] h2 {
        color: #6b4423;
    }

    /* Headers */
    h1 {
        color: #6b4423;
        font-weight: 700;
        padding: 1.5rem 0.5rem;
        text-shadow: 1px 1px 2px rgba(139, 111, 71, 0.1);
        text-align: center;
        background: linear-gradient(135deg, #fff8f0 0%, #f5ead5 50%, #fff8f0 100%);
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(139, 111, 71, 0.1);
        position: relative;
    }

    /* Fall leaves decoration for header */
    h1::before {
        content: "🍂";
        position: absolute;
        left: 20px;
        top: 50%;
        transform: translateY(-50%) rotate(-15deg);
        font-size: 1.5rem;
        opacity: 0.6;
    }

    h1::after {
        content: "🍁";
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%) rotate(15deg);
        font-size: 1.5rem;
        opacity: 0.6;
    }

    h3 {
        color: #8b6f47;
    }

    /* Chat messages */
    .stChatMessage {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(107, 68, 35, 0.08);
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #000000 !important;
    }

    /* User message - light cream with fall border */
    [data-testid="stChatMessageContent"][data-testid*="user"] {
        background-color: #fff8f0 !important;
        border-left: 4px solid #d4895a;
        color: #000000 !important;
    }

    /* Assistant message - warm white with brown border */
    [data-testid="stChatMessageContent"][data-testid*="assistant"] {
        background-color: #ffffff !important;
        border-left: 4px solid #8b6f47;
        color: #000000 !important;
    }

    /* Force assistant message container to white */
    [data-testid="stChatMessage"]:has([data-testid*="assistant"]) {
        background-color: #ffffff !important;
    }

    /* Assistant message avatar container */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #ffffff !important;
    }

    /* All child elements in assistant messages */
    [data-testid*="assistant"] * {
        background-color: transparent !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        width: 100%;
        background-color: #c17344;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(193, 115, 68, 0.2);
    }

    .stButton > button:hover {
        background-color: #a85e35;
        box-shadow: 0 4px 12px rgba(193, 115, 68, 0.3);
    }

    /* Clear buttons - transparent background with border */
    button[kind="secondary"],
    .stButton > button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] .stButton > button[kind="secondary"],
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] button[kind="secondary"],
    .stButton button[type="secondary"],
    .element-container button[kind="secondary"] {
        background-color: transparent !important;
        color: #8b6f47 !important;
        border: 2px solid #d4895a !important;
        box-shadow: none !important;
    }

    button[kind="secondary"]:hover,
    .stButton > button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover,
    [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] button[kind="secondary"]:hover,
    .stButton button[type="secondary"]:hover,
    .element-container button[kind="secondary"]:hover {
        background-color: transparent !important;
        color: #8b6f47 !important;
        border: 2px solid #c17344 !important;
        box-shadow: none !important;
    }

    /* Force text color on all secondary button text and children */
    button[kind="secondary"] *,
    .stButton > button[kind="secondary"] *,
    button[data-testid="baseButton-secondary"] *,
    [data-testid="stSidebar"] button[kind="secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span,
    button[kind="secondary"] div {
        color: #8b6f47 !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e6d5c3;
        background-color: #ffffff;
        color: #000000 !important;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #d4895a;
        box-shadow: 0 0 0 2px rgba(212, 137, 90, 0.1);
    }

    .stTextInput label, .stNumberInput label {
        color: #6b4423 !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        background-color: #ffffff;
        color: #000000 !important;
    }

    .stSelectbox label {
        color: #6b4423 !important;
    }

    .stSelectbox [data-baseweb="select"] {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Dropdown menu options */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }

    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    [role="listbox"] {
        background-color: #ffffff !important;
    }

    [role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    [role="option"]:hover {
        background-color: #fff8f0 !important;
        color: #000000 !important;
    }

    ul[role="listbox"] li {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #fff8f0 !important;
    }

    /* Checkboxes */
    .stCheckbox {
        color: #000000 !important;
    }

    .stCheckbox label {
        color: #000000 !important;
    }

    .stCheckbox span {
        color: #000000 !important;
    }

    /* Markdown text */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #000000 !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #fff8f0;
        border-radius: 8px;
        color: #6b4423;
        font-weight: 600;
    }

    /* Info boxes */
    .stAlert {
        background-color: #fff8f0;
        border-left: 4px solid #d4895a;
        border-radius: 8px;
    }

    /* Success message */
    .stSuccess {
        background-color: #f0f8f0;
        border-left: 4px solid #7fb069;
    }

    /* Divider */
    hr {
        border-color: #e6d5c3;
    }

    /* Caption text */
    .stCaptionContainer, .caption {
        color: #8b6f47;
        text-align: center;
        background: linear-gradient(135deg, #fff8f0 0%, #f5ead5 50%, #fff8f0 100%);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }

    /* Chat input */
    .stChatInput {
        max-width: 900px;
        margin: 0 auto;
        position: relative !important;
        top: 0 !important;
        bottom: auto !important;
    }

    .stChatInputContainer {
        position: relative !important;
        bottom: auto !important;
    }

    [data-testid="stChatInput"] {
        position: relative !important;
        bottom: auto !important;
    }

    .stChatInput > div {
        background-color: #ffffff;
        border: 2px solid #e6d5c3;
        border-radius: 12px;
        margin-bottom: 2rem;
    }

    .stChatInput textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
        caret-color: #000000 !important;
    }

    .stChatInput textarea::placeholder {
        color: #666666 !important;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(135deg, #fff8f0 0%, #f5ead5 50%, #fff8f0 100%);
        padding: 1rem 2rem;
        text-align: center;
        color: #8b6f47;
        font-size: 0.9rem;
        border-top: 2px solid #d4895a;
        box-shadow: 0 -2px 8px rgba(139, 111, 71, 0.1);
        z-index: 999;
    }

    .footer::before {
        content: "🍂 ";
        opacity: 0.6;
    }

    .footer::after {
        content: " 🍁";
        opacity: 0.6;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #c17344;
    }

    /* Sliders */
    .stSlider label {
        color: #6b4423 !important;
    }

    .stSlider [data-baseweb="slider"] {
        color: #000000 !important;
    }

    /* Info/Alert boxes */
    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load saved settings from file
saved_settings = load_settings()

# Initialize session state with saved values or defaults
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_key" not in st.session_state:
    st.session_state.api_key = saved_settings.get("api_key", "")
if "provider" not in st.session_state:
    st.session_state.provider = saved_settings.get("provider", "Anthropic")
if "model" not in st.session_state:
    st.session_state.model = saved_settings.get("model", "")
if "local_host" not in st.session_state:
    st.session_state.local_host = saved_settings.get("local_host", "127.0.0.1")
if "local_port" not in st.session_state:
    st.session_state.local_port = saved_settings.get("local_port", 1337)
if "enable_guardrails" not in st.session_state:
    st.session_state.enable_guardrails = saved_settings.get("enable_guardrails", False)
if "calypso_api_key" not in st.session_state:
    st.session_state.calypso_api_key = saved_settings.get("calypso_api_key", "")
if "temperature" not in st.session_state:
    st.session_state.temperature = saved_settings.get("temperature", 0.7)
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = saved_settings.get("max_tokens", 1024)

# Header with coffee shop vibes
st.title("☕ Ask Our Coffee Shop AI Assistant Anything!")
st.caption("☕ Grab a cup and chat with Claude, GPT, or your local barista bot")

# Sidebar configuration
with st.sidebar:
    st.header("☕ Brew Your Settings")

    # Persistence info
    st.info("💾 Your settings are automatically saved!")

    st.divider()

    # Provider selection
    provider = st.selectbox(
        "🤖 AI Barista",
        ["Anthropic", "OpenAI", "Local"],
        index=["Anthropic", "OpenAI", "Local"].index(st.session_state.provider) if st.session_state.provider in ["Anthropic", "OpenAI", "Local"] else 0,
        key="provider_select"
    )
    if provider != st.session_state.provider:
        st.session_state.provider = provider
        save_current_settings()

    # Local server configuration
    if provider == "Local":
        st.info("🏠 Connect to your local coffee machine (aka AI server)")

        col1, col2 = st.columns([2, 1])
        with col1:
            local_host = st.text_input(
                "Host",
                value=st.session_state.local_host,
                help="Local server host address",
                key="local_host_input"
            )
            if local_host != st.session_state.local_host:
                st.session_state.local_host = local_host
                save_current_settings()

        with col2:
            local_port = st.number_input(
                "Port",
                min_value=1,
                max_value=65535,
                value=st.session_state.local_port,
                help="Local server port",
                key="local_port_input"
            )
            if local_port != st.session_state.local_port:
                st.session_state.local_port = local_port
                save_current_settings()

        # Show the full URL
        local_url = f"http://{local_host}:{local_port}"
        st.caption(f"🌐 Server: `{local_url}`")

    # API Key input
    if provider == "Local":
        api_key = st.text_input(
            "🔑 API Key (Optional)",
            type="password",
            value=st.session_state.api_key,
            help="Some local servers require an API key",
            key="api_key_input"
        )
    else:
        api_key = st.text_input(
            "🔑 API Key",
            type="password",
            value=st.session_state.api_key,
            help=f"Enter your {provider} API key",
            key="api_key_input"
        )
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        save_current_settings()

    # Model selection based on provider
    if provider == "Anthropic":
        anthropic_models = [
            "claude-sonnet-4-5-20250929",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229"
        ]
        default_index = 0
        if st.session_state.model and st.session_state.model in anthropic_models:
            default_index = anthropic_models.index(st.session_state.model)

        model = st.selectbox(
            "🎯 Model",
            anthropic_models,
            index=default_index,
            key="model_select"
        )
    elif provider == "OpenAI":
        openai_models = [
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
        default_index = 0
        if st.session_state.model and st.session_state.model in openai_models:
            default_index = openai_models.index(st.session_state.model)

        model = st.selectbox(
            "🎯 Model",
            openai_models,
            index=default_index,
            key="model_select"
        )
    else:  # Local
        model = st.text_input(
            "🎯 Model Name",
            value=st.session_state.model if st.session_state.model else "local-model",
            help="Enter the model name from your local server",
            key="model_input"
        )

    # Save model if changed
    if model != st.session_state.model:
        st.session_state.model = model
        save_current_settings()

    st.divider()

    # Guardrails Configuration
    st.subheader("🛡️ Content Filter")

    enable_guardrails = st.checkbox(
        "Enable F5 AI Guardrails",
        value=st.session_state.enable_guardrails,
        help="Keep our coffee shop family-friendly",
        key="guardrails_checkbox"
    )
    if enable_guardrails != st.session_state.enable_guardrails:
        st.session_state.enable_guardrails = enable_guardrails
        save_current_settings()

    if enable_guardrails:
        st.info("🔒 All prompts checked for content safety")

        calypso_api_key = st.text_input(
            "F5 AI Guardrails API Key",
            type="password",
            value=st.session_state.calypso_api_key,
            help="Enter your F5 AI Guardrails API key",
            key="calypso_key_input"
        )
        if calypso_api_key != st.session_state.calypso_api_key:
            st.session_state.calypso_api_key = calypso_api_key
            save_current_settings()

    st.divider()

    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        # Temperature slider
        temperature = st.slider(
            "🌡️ Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.temperature,
            step=0.1,
            help="How creative should the AI be?",
            key="temperature_slider"
        )
        if temperature != st.session_state.temperature:
            st.session_state.temperature = temperature
            save_current_settings()

        # Max tokens
        max_tokens = st.slider(
            "📝 Max Tokens",
            min_value=256,
            max_value=4096,
            value=st.session_state.max_tokens,
            step=256,
            help="Maximum response length",
            key="max_tokens_slider"
        )
        if max_tokens != st.session_state.max_tokens:
            st.session_state.max_tokens = max_tokens
            save_current_settings()

    st.divider()

    # Clear chat button
    if st.button("🗑️ Clear Chat History", type="secondary"):
        st.session_state.messages = []
        st.rerun()

    # Clear saved settings button
    if st.button("🔄 Clear Saved Settings", type="secondary"):
        if clear_settings():
            st.success("✅ Settings cleared! Refresh the page to reset.")
            st.session_state.clear()
            st.rerun()

    st.divider()

    # Chat History section
    st.markdown("### 📜 Recent Orders")

    # Get user messages from history
    user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]

    if user_messages:
        # Show last 5 prompts
        recent_prompts = user_messages[-5:][::-1]  # Reverse to show newest first

        for idx, msg in enumerate(recent_prompts):
            # Truncate long messages for display
            display_text = msg["content"][:50] + "..." if len(msg["content"]) > 50 else msg["content"]

            # Create a unique key for each button
            button_key = f"rerun_{idx}_{hash(msg['content'])}"

            if st.button(f"☕ {display_text}", key=button_key, type="secondary"):
                # Store the selected prompt in session state
                st.session_state.rerun_prompt = msg["content"]
                st.rerun()
    else:
        st.caption("No orders yet. Ask me anything!")

    st.divider()

    # About section
    st.markdown("### 🍁 About Our Shop")
    st.markdown("""
    Welcome to our cozy AI coffee shop!

    **Your Baristas:**
    - ☕ Anthropic Claude
    - 🍂 OpenAI GPT
    - 🏠 Local AI Servers
    - 🛡️ F5 Guardrails

    *Serving fresh AI since 2024*
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Guardrails check function
def check_guardrails(prompt: str) -> dict:
    """Check prompt against Calypso AI guardrails"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {st.session_state.calypso_api_key}"
        }

        payload = {
            "input": prompt,
            "model": model if 'model' in locals() else "default"
        }

        response = requests.post(
            "https://www.us1.calypsoai.app/backend/v1/scans",
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            outcome = data.get("result", {}).get("outcome", "flagged")
            is_blocked = (outcome == "flagged")

            return {
                "allowed": not is_blocked,
                "blocked": is_blocked,
                "reason": data.get("reason", "F5 Guardrails Policy Violation" if is_blocked else "Content approved"),
                "categories": data.get("categories", [])
            }
        else:
            # If the API returns an error, log it but don't block (fail open)
            st.warning(f"⚠️ Guardrails check returned status {response.status_code}. Proceeding without check.")
            return {
                "allowed": True,
                "blocked": False,
                "reason": f"API error: {response.status_code}"
            }

    except requests.exceptions.RequestException as e:
        # If there's a connection error, fail open (allow the request)
        st.warning(f"⚠️ Could not connect to guardrails service. Proceeding without check.")
        return {
            "allowed": True,
            "blocked": False,
            "reason": f"Connection error: {str(e)}"
        }
    except Exception as e:
        st.error(f"❌ Guardrails error: {str(e)}")
        return {
            "allowed": False,
            "blocked": True,
            "reason": f"System error: {str(e)}"
        }

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

# User input - handle both new input and rerun requests
prompt = None

# Check if we're rerunning a previous prompt
if hasattr(st.session_state, 'rerun_prompt') and st.session_state.rerun_prompt:
    prompt = st.session_state.rerun_prompt
    st.session_state.rerun_prompt = None  # Clear the rerun flag
else:
    # Get new input from chat
    prompt = st.chat_input("What can I brew up for you today? ☕")

if prompt:
    # Validation
    if provider == "Local":
        if not st.session_state.local_host or not st.session_state.local_port:
            st.error("⚠️ Please configure your local server in the sidebar.")
            st.stop()
    else:
        if not st.session_state.api_key:
            st.error("⚠️ Please enter your API key in the sidebar to get started.")
            st.stop()

    # Check guardrails if enabled
    if st.session_state.enable_guardrails:
        if not st.session_state.calypso_api_key:
            st.error("⚠️ Please enter your Calypso AI API key to use content filtering.")
            st.stop()

        with st.spinner("🛡️ Checking content policy..."):
            guardrails_result = check_guardrails(prompt)

        if guardrails_result["blocked"]:
            st.error(f"🚫 **Sorry mate, that particular brand of coffee is forbidden.**\n\n{guardrails_result['reason']}")
            if guardrails_result.get("categories"):
                st.caption(f"Flagged: {', '.join(guardrails_result['categories'])}")
            st.stop()
        else:
            st.success("✅ Order approved!", icon="☕")

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Brewing your response... ☕"):
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

# Footer
st.markdown(
    """
    <div class="footer">
        Made with love by your local AI experts. ☕
    </div>
    """,
    unsafe_allow_html=True
)
