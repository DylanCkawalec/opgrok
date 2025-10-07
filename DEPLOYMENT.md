# Deployment Guide

This guide covers deploying the Grok + n8n Workflow Automation Platform in various environments.

## 🚀 Local Development

### Quick Start (Recommended)

```bash
# 1. Clone and setup
git clone https://github.com/DylanCkawalec/opgrok.git
cd opgrok
cp .env.example .env
# Edit .env and add your XAI_API_KEY

# 2. Start all services
bash scripts/run_n8n.sh

# 3. Access
# - http://localhost:8000 (Chat)
# - http://localhost:8000/workflows (Workflow Builder)
# - http://localhost:5678 (n8n Dashboard)
```

### Manual Setup (Without Docker)

```bash
# 1. Build Rust CLI
cd grok-chat-app
cargo build --release --features terminal
cd ..

# 2. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r webapp/requirements.txt

# 3. Start n8n separately
npx n8n start --tunnel

# 4. Run webapp
export XAI_API_KEY="your_key"
export N8N_API_URL="http://localhost:5678/api/v1"
python -m uvicorn webapp.app.main:app --reload
```

## 🐳 Docker Deployment

### Using Docker Compose (Production-Ready)

**docker-compose.yml** is already configured for production use.

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with production values

# 2. Build and start
docker-compose up -d --build

# 3. Check status
docker-compose ps
docker-compose logs -f
```

### Environment Variables

Required:
```bash
XAI_API_KEY=xai-xxx                    # Your xAI API key
```

Optional (n8n):
```bash
N8N_BASIC_AUTH_USER=admin              # n8n username
N8N_BASIC_AUTH_PASSWORD=secure_pass    # n8n password (change this!)
N8N_API_URL=http://n8n:5678/api/v1    # Internal URL
N8N_WEBHOOK_URL=http://n8n:5678       # Webhook URL
```

### Production Hardening

1. **Update Secrets**
```bash
# Generate strong password
openssl rand -base64 32

# Update .env
N8N_BASIC_AUTH_PASSWORD=<generated_password>
```

2. **Enable HTTPS**
```yaml
# Add nginx reverse proxy to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./ssl:/etc/nginx/ssl
  depends_on:
    - webapp
    - n8n
```

3. **Configure Firewall**
```bash
# Only expose necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## ☁️ Cloud Deployment

### AWS (EC2 + RDS)

**1. Launch EC2 Instance**
```bash
# t3.medium or larger recommended
# Ubuntu 22.04 LTS
```

**2. Install Dependencies**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose git
sudo usermod -aG docker ubuntu
```

**3. Setup RDS PostgreSQL**
- Create RDS PostgreSQL instance
- Update docker-compose.yml to use RDS endpoint

```yaml
# Remove local postgres service
# Update n8n environment:
environment:
  - DB_TYPE=postgresdb
  - DB_POSTGRESDB_HOST=your-rds-endpoint.rds.amazonaws.com
  - DB_POSTGRESDB_PORT=5432
  - DB_POSTGRESDB_DATABASE=n8n
  - DB_POSTGRESDB_USER=n8n
  - DB_POSTGRESDB_PASSWORD=secure_password
```

**4. Deploy**
```bash
git clone <repo>
cd opgrok
vim .env  # Add secrets
docker-compose up -d
```

**5. Setup Load Balancer (Optional)**
- Create Application Load Balancer
- Configure target groups for port 8000 and 5678
- Add SSL certificate from ACM

### Google Cloud Platform (GKE)

**1. Create Kubernetes Cluster**
```bash
gcloud container clusters create opgrok \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --zone=us-central1-a
```

**2. Create Kubernetes Manifests**

```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opgrok-webapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: opgrok-webapp
  template:
    metadata:
      labels:
        app: opgrok-webapp
    spec:
      containers:
      - name: webapp
        image: gcr.io/your-project/opgrok-webapp:latest
        env:
        - name: XAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: opgrok-secrets
              key: xai-api-key
        ports:
        - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: opgrok-webapp
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: opgrok-webapp
```

**3. Deploy to GKE**
```bash
# Build and push image
docker build -t gcr.io/your-project/opgrok-webapp:latest .
docker push gcr.io/your-project/opgrok-webapp:latest

# Create secrets
kubectl create secret generic opgrok-secrets \
  --from-literal=xai-api-key=$XAI_API_KEY

# Deploy
kubectl apply -f kubernetes/
```

### DigitalOcean (Droplet)

**1. Create Droplet**
```bash
# Ubuntu 22.04, 4GB RAM
# Enable SSH keys
```

**2. Setup Docker**
```bash
ssh root@your-droplet-ip
apt update && apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

**3. Deploy**
```bash
git clone <repo>
cd opgrok
vim .env  # Configure secrets
docker-compose up -d
```

**4. Setup Firewall**
```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```

## 🔒 Security Best Practices

### 1. Secrets Management

**Never commit secrets to git:**
```bash
# Use .env files (gitignored)
# Or use secret management services:

# AWS Secrets Manager
aws secretsmanager get-secret-value \
  --secret-id opgrok/xai-api-key \
  --query SecretString \
  --output text

# HashiCorp Vault
vault kv get secret/opgrok/xai-api-key

# Kubernetes Secrets
kubectl get secret opgrok-secrets -o json
```

### 2. Network Security

```bash
# Use private networks for service communication
# Only expose necessary ports
# Enable TLS/SSL for all external endpoints
```

### 3. Access Control

```yaml
# n8n authentication
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=<strong_password>

# Add OAuth2/OIDC for webapp (future enhancement)
```

### 4. Monitoring & Logging

```yaml
# Add logging service to docker-compose
loki:
  image: grafana/loki:latest
  ports:
    - "3100:3100"
  
grafana:
  image: grafana/grafana:latest
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=admin
```

## 📊 Monitoring

### Health Checks

```bash
# Check webapp
curl http://localhost:8000/api/models

# Check n8n
curl http://localhost:5678/healthz

# Check n8n API
curl -u admin:password http://localhost:5678/api/v1/workflows
```

### Metrics

```bash
# Docker stats
docker-compose stats

# Container logs
docker-compose logs -f webapp
docker-compose logs -f n8n

# PostgreSQL stats
docker-compose exec postgres psql -U n8n -c "SELECT * FROM pg_stat_activity;"
```

## 🔄 Backup & Recovery

### Backup n8n Data

```bash
# Backup database
docker-compose exec postgres pg_dump -U n8n n8n > backup-$(date +%Y%m%d).sql

# Backup n8n data directory
docker run --rm -v opgrok_n8n_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/n8n-data-$(date +%Y%m%d).tar.gz /data
```

### Restore

```bash
# Restore database
cat backup-20250101.sql | docker-compose exec -T postgres psql -U n8n n8n

# Restore data directory
docker run --rm -v opgrok_n8n_data:/data -v $(pwd):/backup \
  alpine tar xzf /backup/n8n-data-20250101.tar.gz -C /
```

## 📈 Scaling

### Horizontal Scaling (Multiple Instances)

1. **Use external PostgreSQL** (RDS, Cloud SQL, etc.)
2. **Use Redis for session storage** (instead of in-memory)
3. **Load balance multiple webapp instances**
4. **Use n8n queue mode** for distributed processing

```yaml
# docker-compose.scale.yml
services:
  webapp:
    deploy:
      replicas: 3
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
  
  n8n-worker:
    image: n8nio/n8n:latest
    environment:
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
    deploy:
      replicas: 3
```

### Vertical Scaling

```bash
# Increase resources in docker-compose.yml
services:
  webapp:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
  
  n8n:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

## 🐛 Troubleshooting

### Common Issues

**1. n8n not accessible**
```bash
# Check if container is running
docker-compose ps

# Check logs
docker-compose logs n8n

# Restart
docker-compose restart n8n
```

**2. Webapp can't connect to n8n**
```bash
# Check network
docker-compose exec webapp ping n8n

# Verify environment variables
docker-compose exec webapp env | grep N8N
```

**3. Out of disk space**
```bash
# Clean up Docker
docker system prune -a

# Check volume usage
docker volume ls
du -sh /var/lib/docker/volumes/*
```

## 📞 Support

- Documentation: See README.md and other docs
- Issues: https://github.com/DylanCkawalec/opgrok/issues
- n8n Docs: https://docs.n8n.io
- xAI Docs: https://docs.x.ai

## 📝 License

See LICENSE file for details.
