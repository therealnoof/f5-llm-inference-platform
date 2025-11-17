# F5 LLM Inference Platform - Deployment Guide

This guide provides step-by-step instructions for deploying the F5 LLM Inference Streamlit application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API keys for LLM providers:
  - Anthropic API key (get from: https://console.anthropic.com/)
  - OpenAI API key (get from: https://platform.openai.com/api-keys)

## Local Development Setup

### 1. Clone or Download the Repository

```bash
cd /path/to/your/project
```

### 2. Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

**On macOS:**
```bash
pip3 install -r requirements.txt
```

**On Linux/Windows (or if inside a virtual environment):**
```bash
pip install -r requirements.txt
```

**Note for macOS users:** If you get a warning about scripts not being on PATH, add this to your `~/.zshrc` or `~/.bash_profile`:
```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
```
Then run `source ~/.zshrc` (or `source ~/.bash_profile`) to apply the changes.

### 4. Set Up Environment Variables (Optional)

Create a `.env` file in the project root to store your API keys securely:

```bash
touch .env
```

Add your API keys to `.env`:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** You can also enter API keys directly in the app's sidebar interface.

### 5. Run the Application

**If using a virtual environment (recommended):**
```bash
streamlit run app.py
```

**On macOS without virtual environment:**
```bash
python3 -m streamlit run app.py
```
Or, if you added the Python bin directory to your PATH:
```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

## Deployment Options

### Option 1: Streamlit Community Cloud (Free)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch, and main file (`app.py`)
   - Add your API keys in "Advanced settings" > "Secrets":
     ```toml
     ANTHROPIC_API_KEY = "your_key_here"
     OPENAI_API_KEY = "your_key_here"
     ```
   - Click "Deploy"

### Option 2: Docker Deployment

#### Option 2a: Pull Pre-built Image from Docker Hub (Fastest)

**This is the easiest method - no building required!**

1. **Pull the image from Docker Hub:**

```bash
docker pull YOUR_USERNAME/coffee-ai-guardrails:latest
```

2. **Run the container:**

```bash
# Basic run (settings won't persist)
docker run -p 8501:8501 YOUR_USERNAME/coffee-ai-guardrails:latest

# Run with persistent settings
docker run -p 8501:8501 \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  YOUR_USERNAME/coffee-ai-guardrails:latest

# Run in detached mode (background)
docker run -d -p 8501:8501 \
  --name coffee-ai-app \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  YOUR_USERNAME/coffee-ai-guardrails:latest

# Run with API keys pre-configured
docker run -d -p 8501:8501 \
  --name coffee-ai-app \
  -e ANTHROPIC_API_KEY=your_anthropic_key \
  -e OPENAI_API_KEY=your_openai_key \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  YOUR_USERNAME/coffee-ai-guardrails:latest
```

3. **Access the app at:** `http://localhost:8501`

4. **Manage the container:**

```bash
# View running containers
docker ps

# Stop the container
docker stop coffee-ai-app

# Start the container again
docker start coffee-ai-app

# View logs
docker logs coffee-ai-app

# Follow logs in real-time
docker logs -f coffee-ai-app

# Remove the container
docker rm coffee-ai-app
```

#### Option 2b: Build Your Own Docker Image

1. **Clone the repository:**

```bash
git clone https://github.com/therealnoof/f5-llm-inference-platform.git
cd f5-llm-inference-platform
```

2. **Build the Docker image:**

```bash
docker build -t f5-llm-inference .
```

3. **Run the container:**

```bash
# Basic run
docker run -p 8501:8501 f5-llm-inference

# Run with environment variables
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  f5-llm-inference

# Run in detached mode with persistent settings
docker run -d -p 8501:8501 \
  --name coffee-ai-app \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  -v ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json \
  f5-llm-inference
```

4. **Access the app at:** `http://localhost:8501`

#### Docker Compose (Advanced)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  coffee-ai:
    image: YOUR_USERNAME/coffee-ai-guardrails:latest
    ports:
      - "8501:8501"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ~/.coffee_ai_settings.json:/root/.coffee_ai_settings.json
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

Stop with:
```bash
docker-compose down
```

### Option 3: AWS EC2 Deployment

1. **Launch an EC2 instance** (Ubuntu 22.04 recommended)

2. **SSH into your instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

4. **Clone your repository:**
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

5. **Set up virtual environment and install packages:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. **Run with nohup (background process):**
```bash
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

7. **Configure security group** to allow inbound traffic on port 8501

8. **Access the app at:** `http://your-ec2-ip:8501`

### Option 4: Google Cloud Run

1. **Create a Dockerfile** (see Docker deployment section)

2. **Build and push to Google Container Registry:**
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/f5-llm-inference
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy f5-llm-inference \
  --image gcr.io/YOUR_PROJECT_ID/f5-llm-inference \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your_key,OPENAI_API_KEY=your_key
```

### Option 5: Azure Container Instances

1. **Build Docker image** (see Docker deployment section)

2. **Push to Azure Container Registry:**
```bash
az acr build --registry <your-registry-name> --image f5-llm-inference .
```

3. **Deploy to Azure Container Instances:**
```bash
az container create \
  --resource-group <your-resource-group> \
  --name f5-llm-inference \
  --image <your-registry-name>.azurecr.io/f5-llm-inference \
  --dns-name-label f5-llm-app \
  --ports 8501 \
  --environment-variables \
    ANTHROPIC_API_KEY=your_key \
    OPENAI_API_KEY=your_key
```

## Configuration

### Custom Port

To run on a different port:
```bash
streamlit run app.py --server.port=8080
```

### Production Settings

For production deployments, consider adding to `~/.streamlit/config.toml`:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** or secrets management services
3. **Enable HTTPS** for production deployments
4. **Implement rate limiting** if exposing publicly
5. **Regular dependency updates:** `pip install --upgrade -r requirements.txt`
6. **Use `.gitignore`** to exclude sensitive files:
   ```
   .env
   venv/
   __pycache__/
   *.pyc
   .streamlit/secrets.toml
   ```

## Troubleshooting

### "pip: command not found" on macOS
Use `pip3` instead of `pip`:
```bash
pip3 install -r requirements.txt
```

### "streamlit: command not found" on macOS
Use the Python module syntax:
```bash
python3 -m streamlit run app.py
```
Or add Python's bin directory to your PATH (see installation instructions above).

### Port Already in Use
```bash
# Find and kill the process using port 8501
lsof -ti:8501 | xargs kill -9
```

### Module Not Found Error
```bash
# Ensure you're in the virtual environment and reinstall
# On macOS:
pip3 install -r requirements.txt
# On Linux/Windows or in venv:
pip install -r requirements.txt
```

### API Key Errors
- Verify your API key is valid
- Check for extra spaces or newlines in your key
- Ensure the key has proper permissions

## Usage

1. Open the application in your browser
2. Select your LLM provider from the sidebar (Anthropic or OpenAI)
3. Enter your API key in the sidebar
4. Choose your preferred model
5. Adjust temperature and max tokens as needed
6. Start chatting with the AI assistant

## Support

For issues or questions:
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Review [Anthropic API docs](https://docs.anthropic.com)
- Review [OpenAI API docs](https://platform.openai.com/docs)

## License

This project is provided as-is for demonstration purposes.
