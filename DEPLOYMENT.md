# Cloud Deployment Guide

Deploy the KPI Intelligence Platform to major cloud providers.

## 🌐 Deployment Options Overview

| Platform | Difficulty | Cost | Scalability | Best For |
|----------|-----------|------|-------------|----------|
| Heroku | ⭐ Easy | $ Low | ⭐⭐ Medium | Quick demos, small teams |
| AWS EC2 | ⭐⭐ Medium | $$ Medium | ⭐⭐⭐ High | Full control, custom setup |
| Google Cloud Run | ⭐ Easy | $ Low | ⭐⭐⭐ High | Serverless, auto-scaling |
| Azure Container | ⭐⭐ Medium | $$ Medium | ⭐⭐⭐ High | Enterprise, MS ecosystem |
| DigitalOcean | ⭐ Easy | $ Low | ⭐⭐ Medium | Simple, affordable |

## 🔥 Heroku (Easiest - 5 minutes)

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deployment Steps

1. **Create `Procfile`**
```bash
cat > Procfile << EOF
web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0
EOF
```

2. **Initialize Git (if not already)**
```bash
git init
git add .
git commit -m "Initial commit"
```

3. **Create Heroku app**
```bash
heroku login
heroku create kpi-platform-yourname
```

4. **Deploy**
```bash
git push heroku main
```

5. **Open app**
```bash
heroku open
```

### Configuration
```bash
# Scale dynos
heroku ps:scale web=1

# View logs
heroku logs --tail

# Set environment variables
heroku config:set STREAMLIT_SERVER_HEADLESS=true
```

## ☁️ AWS EC2 (Full Control)

### Prerequisites
- AWS account
- EC2 instance running Ubuntu 22.04
- SSH key pair

### Deployment Steps

1. **Connect to EC2**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

2. **Install dependencies**
```bash
sudo apt update
sudo apt install -y python3.11 python3-pip git

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

3. **Clone repository**
```bash
git clone <your-repo-url>
cd kpi-intelligence-platform
```

4. **Setup application**
```bash
./setup.sh
```

5. **Run with systemd**
Create service file:
```bash
sudo nano /etc/systemd/system/kpi-platform.service
```

Add content:
```ini
[Unit]
Description=KPI Intelligence Platform
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/kpi-intelligence-platform
ExecStart=/home/ubuntu/kpi-intelligence-platform/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Start service**
```bash
sudo systemctl daemon-reload
sudo systemctl start kpi-platform
sudo systemctl enable kpi-platform
sudo systemctl status kpi-platform
```

7. **Setup nginx reverse proxy**
```bash
sudo apt install -y nginx

sudo nano /etc/nginx/sites-available/kpi-platform
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/kpi-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Setup SSL with Let's Encrypt**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🚀 Google Cloud Run (Serverless)

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Deployment Steps

1. **Authenticate**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Build container**
```bash
# Build and submit to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kpi-platform
```

3. **Deploy to Cloud Run**
```bash
gcloud run deploy kpi-platform \
  --image gcr.io/YOUR_PROJECT_ID/kpi-platform \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10
```

4. **Get URL**
```bash
gcloud run services describe kpi-platform --region us-central1 --format='value(status.url)'
```

### Benefits
- ✅ Auto-scaling (0 to N instances)
- ✅ Pay only for actual usage
- ✅ Automatic HTTPS
- ✅ No server management

## 🔷 Azure Container Instances

### Prerequisites
- Azure account
- Azure CLI installed

### Deployment Steps

1. **Login**
```bash
az login
```

2. **Create resource group**
```bash
az group create --name kpi-platform-rg --location eastus
```

3. **Build and push to ACR**
```bash
# Create container registry
az acr create --resource-group kpi-platform-rg \
  --name kpiplatformacr --sku Basic

# Login to ACR
az acr login --name kpiplatformacr

# Build and push
docker build -t kpi-platform:latest .
docker tag kpi-platform:latest kpiplatformacr.azurecr.io/kpi-platform:latest
docker push kpiplatformacr.azurecr.io/kpi-platform:latest
```

4. **Deploy container**
```bash
az container create \
  --resource-group kpi-platform-rg \
  --name kpi-platform \
  --image kpiplatformacr.azurecr.io/kpi-platform:latest \
  --dns-name-label kpi-platform-unique \
  --ports 8501 \
  --cpu 2 \
  --memory 4
```

5. **Get URL**
```bash
az container show \
  --resource-group kpi-platform-rg \
  --name kpi-platform \
  --query ipAddress.fqdn
```

## 🌊 DigitalOcean App Platform

### Prerequisites
- DigitalOcean account

### Deployment Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy to DigitalOcean"
git push origin main
```

2. **Via DigitalOcean Console**
- Go to App Platform
- Click "Create App"
- Select GitHub repository
- Choose branch: `main`
- DigitalOcean auto-detects Dockerfile
- Click "Next" → "Launch App"

3. **Configure**
- Set environment variables in App Settings
- Configure domain (optional)
- Enable autoscaling

## 📊 Performance Optimization for Production

### 1. Database Integration
For persistent storage, add PostgreSQL:

```python
# In app.py
import psycopg2

conn = psycopg2.connect(
    host="your-db-host",
    database="kpi_platform",
    user="user",
    password="password"
)
```

### 2. Caching
Enable Redis for better performance:

```bash
pip install redis streamlit-redis-cache
```

```python
import redis
from streamlit_redis_cache import get_cache

cache = get_cache("localhost:6379")
```

### 3. Load Balancing
Use multiple instances behind load balancer:

**AWS Application Load Balancer**
```bash
aws elbv2 create-load-balancer \
  --name kpi-platform-lb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx
```

### 4. Monitoring
Add application monitoring:

```bash
pip install prometheus-client
```

```python
from prometheus_client import Counter, Histogram
import streamlit as st

request_count = Counter('app_requests_total', 'Total requests')
```

## 🔐 Security Best Practices

### 1. Environment Variables
Never commit secrets. Use environment variables:

```bash
# .env file (add to .gitignore)
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
API_KEY=your-api-key
```

Load in app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

### 2. Authentication
Add authentication layer:

```bash
pip install streamlit-authenticator
```

```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Your app here
    pass
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

### 3. HTTPS
Always use HTTPS in production:
- Heroku: Automatic
- AWS/GCP/Azure: Use load balancer with SSL certificate
- Let's Encrypt: Free SSL certificates

## 📈 Scaling Strategies

### Horizontal Scaling
Run multiple instances:

**Docker Swarm**
```bash
docker swarm init
docker service create \
  --name kpi-platform \
  --replicas 3 \
  -p 8501:8501 \
  kpi-platform:latest
```

**Kubernetes**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kpi-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kpi-platform
  template:
    metadata:
      labels:
        app: kpi-platform
    spec:
      containers:
      - name: kpi-platform
        image: kpi-platform:latest
        ports:
        - containerPort: 8501
```

### Vertical Scaling
Increase resources:

```bash
# Heroku
heroku ps:resize web=standard-2x

# AWS EC2
# Use larger instance type (t3.large → t3.xlarge)

# Google Cloud Run
gcloud run services update kpi-platform \
  --memory 4Gi \
  --cpu 4
```

## 💰 Cost Optimization

### Estimates (Monthly)

**Heroku**
- Free tier: $0 (limited hours)
- Hobby: $7/dyno
- Standard: $25-50/dyno

**AWS EC2**
- t3.micro: ~$8
- t3.small: ~$15
- t3.medium: ~$30

**Google Cloud Run**
- Pay per request: ~$5-20 for small apps
- Free tier: 2M requests/month

**Azure Container Instances**
- 1 vCPU, 2GB RAM: ~$35

**DigitalOcean**
- Basic Droplet: $6-12
- App Platform: $5-12

## 📞 Support & Resources

- **AWS**: https://aws.amazon.com/documentation/
- **Google Cloud**: https://cloud.google.com/docs
- **Azure**: https://docs.microsoft.com/azure/
- **Heroku**: https://devcenter.heroku.com/
- **DigitalOcean**: https://docs.digitalocean.com/

---

**Choose the platform that best fits your needs and budget!** 🚀
