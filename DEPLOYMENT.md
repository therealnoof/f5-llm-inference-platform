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

```bash
pip install -r requirements.txt
```

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

1. **Create a Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run the Docker container:**

```bash
# Build the image
docker build -t f5-llm-inference .

# Run the container
docker run -p 8501:8501 \
  -e ANTHROPIC_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  f5-llm-inference
```

3. **Access the app at:** `http://localhost:8501`

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

### Port Already in Use
```bash
# Find and kill the process using port 8501
lsof -ti:8501 | xargs kill -9
```

### Module Not Found Error
```bash
# Ensure you're in the virtual environment and reinstall
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
