# Observian

**Scalable System Monitoring and Metrics Platform**

Observian is a containerized, production-grade backend platform designed for real-time monitoring of microservices, system uptime, and error rates. Inspired by enterprise-grade data systems, it emphasizes clean architecture, traceability, and modularity.

## 🚀 Project Overview

Observian simulates real-world platform engineering challenges by offering:

- Centralized log ingestion and querying
- GitHub event monitoring via background ingestion
- API-driven control and metrics exposure
- Prometheus/Grafana integration for observability
- Scalable, containerized architecture with CI/CD readiness

---

## 🛠 Architecture & Tech Stack

| Component      | Stack / Tool                              |
|----------------|-------------------------------------------|
| Backend        | FastAPI (Python 3.9), SQLAlchemy, Pydantic |
| Database       | PostgreSQL (Star schema, partitions, indexes) |
| Metrics        | Prometheus for scraping, Grafana for dashboards |
| Containerization | Docker & Docker Compose (Kubernetes-ready) |
| CI/CD Ready    | Render, AWS, or GCP compatible setup       |
| Config & Tools | Python-dotenv, `requests`, `logging`       |

---

## 🔑 Key Features

- **RESTful APIs** for logs, summaries, live feeds, and system control
- **GitHub Ingestor**: Async background worker fetches and logs GitHub events
- **Prometheus Metrics**: Request count, latency, and error rate tracking
- **Log Pruning**: Automatic and manual pruning support
- **Health Monitoring**: `/health` and `/control/ingestor-health` endpoints
- **Secure Control**: API key protected endpoints for sensitive operations
- **Modular Design**: Clear separation between core logic, services, and workers

---

## 📁 Data Model

- **Fact Table**: `log_events`  
  *(id, service_id, timestamp, status_code, event_type, latency_ms)*

- **Dimension Table**: `services`  
  *(id, name, team_owner)*

> Designed to scale with support for RBAC and additional dimensions.

---

## 📡 API Endpoints

| Endpoint                       | Description                                 |
|--------------------------------|---------------------------------------------|
| `GET /logs`                   | Filter logs by service, status, event type, time |
| `GET /logs/summary`          | Aggregated log stats                        |
| `GET /logs/live-feed`        | Latest N logs for live dashboards           |
| `POST /logs`                 | Create a new log entry                      |
| `GET /control/ingestor-status` | Check GitHub ingestor state                |
| `POST /control/ingestor-toggle` | Toggle ingestor on/off (API key required) |
| `GET /control/ingestor-health` | Validate background task is running        |
| `POST /control/prune`        | Manually prune old logs (API key required)  |
| `GET /metrics`               | Prometheus-compatible metrics               |
| `GET /health`                | API liveness check                          |

---

## ⚙️ Background Workers

- **GitHub Ingestor**: Async worker fetches public GitHub events and posts to `/logs`.
- **Log Pruner**: Periodically removes logs older than N days.

---

## 🔐 Security & Reliability

- **API Key Auth** for control endpoints
- **Thread-safe** state for background worker toggling
- **Error-handling** with consistent logging and responses

---

## 🚀 Deployment

### Using Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/observian.git
cd observian

# Set up environment
cp .env.example .env

# Start the system
docker-compose up --build

> Includes API, PostgreSQL, Prometheus, Grafana, and background workers.
```

### System Boots With:

* DB wait + migrations
* Service table seeding
* FastAPI startup
* Prometheus & Grafana preconfigured

---

## 🧪 Development & Testing

* Modular structure: `api/`, `models/`, `services/`, `workers/`
* Logging: Uniform across background and API processes
* Test Scripts: For log pruning, DB connectivity

---

## 📊 Sample Use Cases

* Real-time service dashboard with Prometheus and Grafana
* GitHub activity pipeline for monitoring dev team behavior
* Auto-pruned, scalable log storage for infrastructure teams
* System control via secure endpoints (toggle/prune workers)

---

## 🧠 Notable Challenges Solved

* **Async Task Control via API**: Start/stop background tasks securely
* **Structured, Fast Log Ingestion**: Indexed PostgreSQL with partitioning
* **Integrated Observability**: `/metrics`, health checks, Grafana-ready

---

## 👀 Future Enhancements

* Frontend dashboard (in progress)
* RBAC system for user-level filtering
* Webhook/event-stream ingestion
* OAuth for admin dashboard

---

## 📌 Frontend Note

The frontend for Observian is built using **React & Next.js**, currently deployed in Firebase AI tools. It connects to the above API endpoints for log visualization and control. Deployment is optional and can be customized.

---

## 🧑‍💻 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

## 📄 License

MIT License. See `LICENSE.md` for more information.
