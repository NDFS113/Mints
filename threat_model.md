# Threat Model

## Asset: Sensor Node

- **Threat**: Compromise by attacker.
- **Mitigation**: Sandbox, no-exec partition, non-root user, minimal OS.

## Asset: Backend Database

- **Threat**: Data leak.
- **Mitigation**: IP hashing, limited retention, strict access control.

## Asset: Telemetry

- **Threat**: Interception.
- **Mitigation**: TLS encryption for all transit.
