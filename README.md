markdown

# 📡 IoT Telemetry Monitoring & Logging Pipeline

An end-to-end containerized IoT telemetry ingestion, persistent storage, real-time visualization, and secure zero-trust remote monitoring stack built with **Docker Compose**.
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Node-RED](https://img.shields.io/badge/Node--RED-8F0000?style=for-the-badge&logo=nodered&logoColor=white)
![Cloudflare](https://img.shields.io/badge/Cloudflare_Tunnel-F38020?style=for-the-badge&logo=cloudflare&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🏗️ System Architecture

The following diagram illustrates how telemetry data flows from edge devices to persistent storage, visualization, and secure public access:

```mermaid
flowchart LR
    subgraph Edge["Edge / Field Devices"]
        Sensors["IoT Sensors & Telemetry"]
    end
    subgraph DockerHost["Docker Host"]
        direction TB
        subgraph Ingestion["Ingestion Layer"]
            PyApp["Python Ingestion Service"]
            NodeRed["Node-RED Engine"]
        end
        subgraph Storage["Storage Layer"]
            MySQL[("MySQL 8.0 Database")]
        end
        subgraph Observability["Observability"]
            Grafana["Grafana Dashboard"]
            Promtail["Promtail Log Collector"]
        end
        subgraph Security["Zero Trust Remote Access"]
            CFTunnel["Cloudflare Tunnel"]
        end
    end
    subgraph Remote["Remote Users"]
        Clients["Admin Dashboard / Client"]
    end
    Sensors -->|"MQTT / HTTP"| PyApp
    Sensors -->|"MQTT / REST"| NodeRed
    PyApp -->|"Store Data"| MySQL
    NodeRed -->|"Store & Stream"| MySQL
    MySQL -->|"Query Metrics"| Grafana
    Promtail -->|"Scrape Logs"| Grafana
    Grafana --- CFTunnel
    CFTunnel ---|"Encrypted Tunnel"| Clients
✨ Key Features
Microservices Orchestration: Fully managed multi-container environment via docker-compose.yml with isolated internal bridge networking (es405-network).
Data Ingestion & Transformation: Python service with automated timezone adjustment (Asia/Jakarta) and Node-RED for dynamic low-code workflow logic.
Persistent Storage: MySQL 8.0 relational database with dedicated initialization scripts and persistent volume management.
Glassmorphism Dashboard: Customized Grafana UI with rich CSS styling (glassmorphism.css) and real-time dashboard panels.
Centralized Container Logging: Promtail agent automatically discovers and scrapes container logs via the Docker socket.
Zero-Trust Remote Access: Integrated Cloudflare Tunnel (cloudflared) providing secure external access without requiring public IP, DDNS, or port forwarding.
DevSecOps Ready: Strict separation of secrets and configuration through .env variable interpolation and robust .gitignore rules.
📁 Repository Structure
text


.
├── src/                        # Python telemetry ingestion & handler logic
│   ├── config.py               # Environment & configuration loader
│   ├── device.py               # IoT device abstractions
│   ├── ispu.py                 # Environmental index calculation (AQMS)
│   ├── mqtt_client.py          # MQTT subscriber & telemetry handler
│   └── main.py                 # Main runtime entrypoint
├── Dockerfile                  # Python container build specification
├── docker-compose.yml          # Multi-service stack orchestration
├── promtail-config.yaml        # Promtail log-scraping configuration
├── requirements.txt            # Python dependencies
├── glassmorphism.css           # Custom Grafana styling
├── .env.example                # Template for environment variables
└── .gitignore                  # Git tracking exclusion list
🚀 Quick Start
1. Prerequisites
Docker Engine
 (v20.10+)
Docker Compose
 (Compose V2)
2. Clone & Configure
Clone the repository to your local machine:

bash


git clone https://github.com/ariefdpras/iot-docker-pipeline.git
cd iot-docker-pipeline
Copy the environment variable template and fill in your actual credentials:

bash


cp .env.example .env
3. Run the Stack
Start all services in detached mode:

bash


docker compose up -d
Check the status of running containers:

bash


docker compose ps
4. Service Endpoints
Service	Local Port	Description
Grafana	http://localhost:3000	Real-time monitoring & metrics visualization
Node-RED	http://localhost:1880	Flow-based visual programming for IoT
MySQL	localhost:3306	Persistent database storage
Promtail	localhost:9080	Log collector agent
👤 Author
Arief Dwi Prasetyo

Role: IT Support | IT Integration | Cloud & DevOps Enthusiast
GitHub: @ariefdpras
```
