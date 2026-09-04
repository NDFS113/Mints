# Deployment Guide

## Prerequisites

- Python 3.9+
- pip
- Virtual Environment

## Installation

1. Clone the repository.
2. `pip install -r requirements.txt`
3. Run `python backend/api.py` for the server.
4. Run `python sensor/start.py` (or individual services) for the sensor.

## Hardening

- Ensure firewall (UFW) blocks all non-essential ports.
- Run as non-root user.
