# CSC468 Project

A containerized web app with a static frontend served by Nginx, a Flask backend API, and a PostgreSQL database for persistent storage. All three communicate over Docker's internal network, with Nginx acting as a reverse proxy.

Built to get hands-on with Docker, container networking, and cloud infrastructure.

## How it works

![System Architecture Diagram](docs/architecture.svg)

- **Frontend (Nginx):** Serves the static HTML, CSS, and JS. Routes any `/api/` request to the backend.
- **Backend (Flask):** Python API running on port 5000. Connects to PostgreSQL for persistent data. Not exposed to the outside world — only reachable through Nginx.
- **Database (PostgreSQL):** Stores log entries with timestamps. Data persists across container restarts via a named Docker volume.
- **Networking:** All three containers live on the same Docker bridge network (`app-network`) and communicate by container name.

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend server | Nginx (alpine) | Lightweight, good for static files and proxying |
| Backend API | Python 3.11 + Flask | Simple and easy to work with for a project this size |
| Database | PostgreSQL 15 (alpine) | Reliable relational DB, native Docker support |
| Orchestration | Docker Compose | Handles networking, startup order, and service config |
| Infrastructure | CloudLab (XenVM) | Provisioned via `profile.py` using the GENI RSpec API |

## Project Structure

```
CSC468-project/
├── profile.py              # CloudLab infrastructure profile
├── docker-compose.yml      # Service orchestration
├── db/
│   └── init.sql            # Table creation and seed data
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf          # Reverse proxy config
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── app.py              # Flask API
```

## API Endpoints

| Endpoint | Method | Returns |
|----------|--------|---------|
| `/api/health` | GET | Backend status, database status, uptime |
| `/api/data` | GET | Container info, environment, stack |
| `/api/entries` | GET | All log entries from the database |
| `/api/entries` | POST | Create a new log entry |
| `/api/entries/<id>` | DELETE | Delete a log entry by id |

## Running it locally

You'll need Docker Desktop installed.

```bash
git clone https://github.com/ethancharest/CSC468-project.git
cd CSC468-project
docker compose up --build
```

Open `http://localhost` in your browser. To stop:

```bash
docker compose down
```

## Running on CloudLab

1. Log into [CloudLab](https://cloudlab.us)
2. Create a new experiment using `profile.py`
3. Wait for the VM to boot — Docker installs and all three containers start automatically
4. Open `http://<node-public-ip>` in your browser

## Build Process

Each service has its own Dockerfile.

**Backend (`backend/Dockerfile`)**

```dockerfile
FROM python:3.11-slim
```
Official lightweight Python image. Smaller than the full image and builds faster.

```dockerfile
WORKDIR /app
```
Sets the working directory inside the container.

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
Copies requirements first to cache the pip install layer — only reruns if `requirements.txt` changes.

```dockerfile
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```
Installs curl for the Docker healthcheck against `/api/health`.

```dockerfile
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["python", "app.py"]
```
Copies the code, exposes port 5000 internally, and starts Flask.

---

**Frontend (`frontend/Dockerfile`)**

```dockerfile
FROM nginx:alpine
```
Lightweight Nginx image, about 20MB.

```dockerfile
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
```
Removes the default Nginx config and drops in our custom one.

```dockerfile
COPY static/ /usr/share/nginx/html/
```
Copies static files into the directory Nginx serves from.

---

**Database**

No custom Dockerfile needed — uses the official `postgres:15-alpine` image directly. On first startup Postgres automatically runs any `.sql` files in `/docker-entrypoint-initdb.d/`, which is how `db/init.sql` creates the entries table and seeds the placeholder.

## Networking

All three containers are on a Docker bridge network called `app-network`. Docker handles DNS resolution by container name, so `nginx.conf` proxies to the backend:

```nginx
proxy_pass http://backend:5000;
```

And Flask connects to Postgres the same way:

```python
host=os.environ.get('DB_HOST', 'db')
```

The backend and database use `expose` instead of `ports` so they are only reachable by other containers on the network. The only public entry point is Nginx on port 80.

## Startup Order

Docker Compose starts the containers in dependency order:

1. PostgreSQL starts and passes its healthcheck (`pg_isready`)
2. Flask starts, connects to the database, and passes its healthcheck (`/api/health`)
3. Nginx starts and begins serving traffic

This prevents Flask from crashing trying to connect to a database that isn't ready yet.

## Resume

[View Resume (PDF)](resume/resume.pdf)