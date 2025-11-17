# Docker Hub Quick Start Guide

Get the F5 Coffee AI Guardrails app running in 2 minutes!

## Prerequisites
- Docker Desktop installed and running

## Quick Start

### 1. Pull the Image

```bash
docker pull YOUR_USERNAME/coffee-ai-guardrails:latest
```

### 2. Run the Container

**Simple (no persistence):**
```bash
docker run -p 8501:8501 YOUR_USERNAME/coffee-ai-guardrails:latest
```

**With persistent settings:**
```bash
docker run -d -p 8501:8501 \
  --name coffee-ai-app \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

**With pre-configured API keys:**
```bash
docker run -d -p 8501:8501 \
  --name coffee-ai-app \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -e OPENAI_API_KEY=sk-... \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

### 3. Access the App

Open your browser to: **http://localhost:8501**

## Container Management

```bash
# View running containers
docker ps

# View logs
docker logs coffee-ai-app

# Follow logs in real-time
docker logs -f coffee-ai-app

# Stop the container
docker stop coffee-ai-app

# Start the container
docker start coffee-ai-app

# Restart the container
docker restart coffee-ai-app

# Remove the container
docker stop coffee-ai-app && docker rm coffee-ai-app
```

## Using Different Ports

If port 8501 is already in use:

```bash
docker run -d -p 8080:8501 \
  --name coffee-ai-app \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

Access at: **http://localhost:8080**

## Docker Compose (Recommended for Production)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  coffee-ai:
    image: YOUR_USERNAME/coffee-ai-guardrails:latest
    container_name: coffee-ai-app
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Create `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

Run:
```bash
docker-compose up -d
```

Stop:
```bash
docker-compose down
```

## Features

- ☕ **Coffee Shop Theme** - Warm, inviting UI with fall colors
- 🤖 **Multiple LLM Providers** - Anthropic Claude & OpenAI GPT
- 🛡️ **Calypso AI Guardrails** - Optional content filtering
- 🏠 **Local Server Support** - Connect to LM Studio, Ollama, etc.
- 💾 **Settings Persistence** - Your preferences are saved
- 🎨 **Clean Interface** - Centered chat, wide mode, no distractions

## Troubleshooting

**Port already in use?**
```bash
# Find what's using port 8501
lsof -i :8501

# Use a different port
docker run -p 8080:8501 YOUR_USERNAME/coffee-ai-guardrails:latest
```

**Container won't start?**
```bash
# Check logs
docker logs coffee-ai-app

# Remove and recreate
docker rm -f coffee-ai-app
docker run -d -p 8501:8501 --name coffee-ai-app YOUR_USERNAME/coffee-ai-guardrails:latest
```

**Settings not persisting?**
Make sure you're using the volume mount:
```bash
-v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json
```

## Advanced Configuration

### Custom Streamlit Config

Create `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

Mount it:
```bash
docker run -d -p 8501:8501 \
  -v $(pwd)/.streamlit:/root/.streamlit \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

### Enable Guardrails

Set the Calypso AI API endpoint in the app UI or via environment variable:
```bash
docker run -d -p 8501:8501 \
  -e CALYPSO_API_URL=https://your-calypso-endpoint \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

## Support

- **GitHub Repository:** https://github.com/therealnoof/f5-llm-inference-platform
- **Full Deployment Guide:** See `DEPLOYMENT.md`
- **Guardrails Testing:** See `GUARDRAILS_TESTING.md`

## License

Provided as-is for demonstration purposes.
