# Deployment Guide - Edge-TTS Synthesizer

This project is a Streamlit application. Here are the best ways to deploy it.

## Option 1: Streamlit Community Cloud (Easiest & Free)
The fastest way to deploy is using Streamlit's own cloud platform.

1.  **Push your code** to a public GitHub repository.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Connect your GitHub account.
4.  Select your repository, branch (`main`), and main file (`app.py`).
5.  Click **Deploy**.

## Option 2: Docker Deployment (Recommended for Production)
For more control and scalability, you can use Docker.

### 1. Create a Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Build and Run
```bash
docker build -t edge-tts-synthesizer .
docker run -p 8501:8501 edge-tts-synthesizer
```

### 3. Deploy to Cloud
You can deploy this Docker container to:
- **Google Cloud Run:** Serverless, scales to zero, very cost-effective.
- **AWS App Runner:** Easiest way to run containers on AWS.
- **DigitalOcean App Platform:** Simple Git-to-deploy for containers.

## Option 3: VPS (Ubuntu/Debian)
If you have a server (like a DigitalOcean Droplet), you can run it as a service.

1.  **Install requirements:** `pip install -r requirements.txt`
2.  **Use PM2 or Systemd** to keep the process running:
    ```bash
    # Example using PM2
    pm2 start "streamlit run app.py" --name "tts-app"
    ```
3.  **Reverse Proxy with Nginx:** Use Nginx to handle SSL (HTTPS) and route traffic to port 8501.

## Important Considerations
- **Internet Access:** The application requires an active internet connection to communicate with Microsoft Edge's TTS servers.
- **Ephemeral Storage:** If you save files locally (e.g., `synthesized_audio.mp3`), they will be lost when the container restarts on platforms like Cloud Run. Use the "Download" button to let users save files to their own devices.
