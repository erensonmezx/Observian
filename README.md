# Failsight: Scalable System Monitoring and Metrics Platform

Failsight is a lightweight, containerized backend platform designed to monitor service performance, system uptime, and error rates in real-time. Built with FastAPI, PostgreSQL, and Prometheus, Failsight simulates the data engineering challenges faced by platform teams: modeling logs, curating high-volume system data, and exposing key metrics for observability.

> Inspired by platform architecture patterns and Goldman Sachs’ open-source data platform (Legend), Failsight emphasizes clean data modeling, traceability, access logic, and system reliability.

---
git ps
## 📦 Tech Stack

- **FastAPI** – REST API for serving log and status data
- **PostgreSQL** – Star schema modeling of logs and system metadata
- **Prometheus** – Custom metrics collection from services
- **Grafana** – Dashboard visualization for alerts and performance monitoring
- **Docker** – Containerization for all services
- **Kubernetes (Optional)** – Local orchestration and Helm-ready structure

---

## Key Features

- ✅ **REST API Endpoints** to fetch system logs, status events, and uptime data with filtering and pagination
- ✅ **Structured Logging** into PostgreSQL using a star schema design with indexing and partitions
- ✅ **Prometheus Integration** for exposing `/metrics` from the API
- ✅ **Grafana Dashboards** for real-time monitoring and alert thresholds (e.g., request latency, error rate)
- ✅ **Planned RBAC Simulation** to mimic role-based access to logs (entitlement modeling)
- ✅ **Modular Design** to support further event ingestion (Kafka/NATS) or external data sources

---

## Data Model Overview

**Star Schema Tables**:
- `log_events` – central fact table storing errors, requests, and response times
- `services` – dimension table for service names, types, and owners
- `users` – optional dimension for role-based filters (planned)

Includes:
- Partitioning on `log_events.timestamp`
- Indexing on `service_id`, `status`, `error_code`

---

## REST API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/logs` | GET | Fetch logs filtered by service, date, severity |
| `/status` | GET | Aggregated health status by service |
| `/metrics` | GET | Prometheus-compatible metrics |
| `/health` | GET | API health check |

Supports query params for filtering, sorting, pagination.

---

## Dashboards & Alerts

- **Grafana Panel**: Shows live request latency, error counts, service uptime
- **Alerts**: Triggered on sustained high error rate, request spike, or API downtime

---

## To Get Started

1. Clone this repo
2. Run `docker-compose up`
3. Visit `localhost:3000/docs` for API
4. Visit `localhost:9090` (Prometheus), `localhost:3001` (Grafana)

---

## Roadmap

- [ ] Add role-based data filtering (RBAC simulation)
- [ ] Add service-to-service alert mapping
- [ ] Add support for message queue ingestion (Kafka/NATS)
- [ ] Convert to Kubernetes-native stack with Helm

---

## 👨‍💻 Author

**Eren Sonmez**  
Email: ernsonmez@gmail.com  
[LinkedIn](https://linkedin.com/in/erensonmez1) | [GitHub](https://github.com/erensonmezx)

---

## 📄 License

MIT – Free for educational and professional portfolio use.