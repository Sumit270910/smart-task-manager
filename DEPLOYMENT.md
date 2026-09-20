# Deployment Guide - Smart Task Manager

This guide walks you through deploying the **Smart Task Manager** web application to production.

---

## 🚀 Option 1: Deploy to Render (Recommended)

Render is the best platform for this project because it natively supports **persistent WebSockets** (enabling real-time updates via Flask-SocketIO) and provides a **free PostgreSQL database**.

### Method A: 1-Click Blueprint Deploy
1. Push your latest code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Configure deployment"
   git push origin main
   ```
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** → **Blueprint**.
4. Connect your GitHub repository (`Sumit270910/smart-task-manager`).
5. Render will automatically read `render.yaml`, provision the PostgreSQL database, configure the environment variables, and build the Python web service!
6. Click **Apply**. Once built, your app will be live with full real-time WebSocket support!

### Method B: Manual Dashboard Deploy
1. **Create PostgreSQL Database**:
   - Go to Render Dashboard → **New +** → **PostgreSQL**.
   - Name: `task-manager-db`.
   - Click **Create Database**.
   - Copy the **Internal Database URL** (or External URL).
2. **Create Web Service**:
   - Click **New +** → **Web Service**.
   - Connect your repository.
   - Set **Runtime**: `Python 3`.
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `gunicorn -k gthread --threads 10 -w 1 app:app`
   - Under **Environment Variables**, add:
     - `SECRET_KEY`: `<generate-a-random-secret-key>`
     - `DATABASE_URL`: `<paste-copied-database-url>`
     - `PYTHON_VERSION`: `3.12.0`
   - Click **Create Web Service**.

---

## ⚡ Option 2: Deploy to Vercel

Vercel deploys the application as serverless functions.
*(Note: Because Vercel serverless functions terminate after each request, real-time WebSocket broadcasting falls back to standard HTTP fetch & page reload, which is fully supported.)*

### Prerequisites for Vercel
Vercel is stateless and has a read-only filesystem, so you need a cloud PostgreSQL database:
- Create a free database on [Neon.tech](https://neon.tech/) or [Supabase](https://supabase.com/).
- Copy your PostgreSQL connection string (`postgresql://...`).

### Steps to Deploy on Vercel:
1. Push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Setup deployment"
   git push origin main
   ```
2. Open [Vercel Dashboard](https://vercel.com/) and click **Add New...** → **Project**.
3. Import your GitHub repository `smart-task-manager`.
4. In the project configuration screen:
   - Framework Preset: **Other**
   - Root Directory: `./`
5. Expand **Environment Variables** and add:
   - `SECRET_KEY`: `<your-random-secret-key>`
   - `DATABASE_URL`: `<your-cloud-postgresql-url>`
6. Click **Deploy**. Vercel will build and launch your application.

---

## 🐳 Option 3: Deploy with Docker & Docker Compose

For deploying on Railway, Fly.io, a VPS (DigitalOcean, Linode, AWS EC2), or running locally with Docker:

### Run with Docker Compose:
```bash
docker-compose up --build -d
```
This will start both PostgreSQL and the Flask application at `http://localhost:5000`.

### Build and run standalone Docker container:
```bash
docker build -t smart-task-manager .
docker run -p 5000:5000 -e DATABASE_URL="postgresql://user:pass@host:5432/dbname" -e SECRET_KEY="your-secret" smart-task-manager
```

---

## 🛠️ Environment Variables Summary

| Variable | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string | Yes (in Cloud) | `sqlite:///task_manager.db` (local fallback) |
| `SECRET_KEY` | Flask session encryption key | Yes | Default fallback key |
| `PORT` | Web port assigned by host | Auto | `5000` |
