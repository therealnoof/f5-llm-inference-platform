# F5 Projects Repository

This repository contains multiple F5-related demonstration and utility applications.

## Projects

### 1. Coffee AI Guardrails (`coffee-ai-guardrails/`)

A beautiful coffee shop-themed LLM inference platform with Calypso AI content filtering.

**Features:**
- ☕ Cozy coffee shop theme with fall colors
- 🤖 Multiple LLM providers (Anthropic Claude, OpenAI GPT)
- 🛡️ Calypso AI guardrails integration
- 🏠 Local server support (LM Studio, Ollama, vLLM)
- 💾 Persistent settings across sessions
- 🎨 Clean, centered chat interface

**Quick Start:**
```bash
cd coffee-ai-guardrails
docker pull YOUR_USERNAME/coffee-ai-guardrails:latest
docker run -p 8501:8501 YOUR_USERNAME/coffee-ai-guardrails:latest
```

**Documentation:**
- [README.md](coffee-ai-guardrails/README.md) - Main documentation
- [DEPLOYMENT.md](coffee-ai-guardrails/DEPLOYMENT.md) - Deployment guide
- [DOCKER_HUB_QUICKSTART.md](coffee-ai-guardrails/DOCKER_HUB_QUICKSTART.md) - Docker deployment
- [BUILD_AND_PUSH.md](coffee-ai-guardrails/BUILD_AND_PUSH.md) - Multi-platform build guide
- [GUARDRAILS_TESTING.md](coffee-ai-guardrails/GUARDRAILS_TESTING.md) - Testing guardrails

**Repository:** https://github.com/therealnoof/f5-llm-inference-platform

---

### 2. Demo Showcase (`demo-showcase/`)

A modern video showcase application for trade shows and demos.

**Features:**
- 📹 Video upload and management
- 🎨 Category organization system
- 🏷️ Tag videos with multiple categories
- 🔍 Filter videos by category
- 📱 Responsive tile-based interface
- ⚙️ Admin panel for content management
- 🎥 Full-screen video player with navigation
- 🌑 Dark theme with F5 branding

**Quick Start:**
```bash
cd demo-showcase
docker compose up --build
```

**Access:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Documentation:**
- [README.md](demo-showcase/README.md) - Full documentation
- [QUICKSTART.md](demo-showcase/QUICKSTART.md) - Quick setup guide

**Repository:** https://github.com/therealnoof/universal-demo-app

---

### 3. Simple MCP Server (`simple-mcp-server/`)

A Model Context Protocol (MCP) server implementation.

**Quick Start:**
```bash
cd simple-mcp-server
# Follow the README in the directory
```

---

## Repository Structure

```
projects/
├── coffee-ai-guardrails/    # Streamlit LLM inference app
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── *.md (documentation)
├── demo-showcase/           # Video showcase application
│   ├── frontend/           # React + TypeScript
│   ├── backend/            # FastAPI
│   └── docker-compose.yml
├── simple-mcp-server/      # MCP server
└── README.md              # This file
```

## Getting Started

Each project has its own README and documentation. Navigate to the project directory and follow the specific instructions.

## Technologies Used

### Coffee AI Guardrails
- Python 3.11
- Streamlit
- Anthropic Claude API
- OpenAI API
- Calypso AI

### Demo Showcase
- **Frontend:** React 18, TypeScript, Tailwind CSS, Vite
- **Backend:** FastAPI, SQLAlchemy, SQLite
- **DevOps:** Docker, Docker Compose, Nginx
- **Video:** MoviePy, Pillow

## License

These projects are provided as-is for demonstration purposes.

## Support

For issues or questions, please refer to the individual project repositories:
- [F5 LLM Inference Platform](https://github.com/therealnoof/f5-llm-inference-platform)
- [Universal Demo App](https://github.com/therealnoof/universal-demo-app)
