# System Architecture

## Sensor Node

- **OS**: Hardened Android or Windows.
- **Runtime**: Python 3.9+.
- **Services**: Telnet (2323), HTTP (8080), SSH (2222), UPnP (1900).
- **Security**: AppArmor/Sandbox isolation.

## Backend

- **Framework**: FastAPI.
- **Database**: SQLite (for MVP) / PostgreSQL (Production).
- **Communication**: TLS encrypted telemetry.
