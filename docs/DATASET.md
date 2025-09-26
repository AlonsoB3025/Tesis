# DATASET Documentation

## Fuente
(Completar manualmente: Elastic Agent, módulos, herramientas, etc.)

## Fecha de adquisición
2025-09-25

## Tamaño & Formato
- Archivos: 10
- Eventos (aprox.): 1719911
- Tamaño total: 267.22 MB
- Formatos detectados: {'csv': 9, 'md': 1}

## Variables principales (detectadas)
- Columnas comunes: No detectadas
- Ejemplo de columnas: @timestamp, agent.name, danger.type, data_stream.dataset, data_stream.namespace, dayofweek, destination.domain, destination.port, etiqueta_binaria, event.action, event.category, event.id, event.reason, event_critical.description, event_critical.event_id, file.extension, file.hash.md5, file.hash.sha1, file.hash.sha256, file.name

## Integridad / Control de versión
SHA256 data/raw: 7d88e248c19b675fb615a5dfbf066b895b578ab290e790dba9553f5f545432a3

## Inventario de archivos
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/Logs-antivirus_etiquetado.csv — 2.60 MB, filas: 6285, formato: csv
  - columnas (muestra): @timestamp, host.ip, host.hostname, rule.name, rule.category, rule.description, file.path, file.hash.md5, file.hash.sha256, danger.type, virus.name
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/DATASET.md — 1.01 KB, filas: None, formato: md
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/logs_antivirus_limpio.csv — 2.54 MB, filas: 6285, formato: csv
  - columnas (muestra): @timestamp, host.ip, host.hostname, rule.name, rule.category, rule.description, file.path, file.hash.md5, file.hash.sha256, danger.type, virus.name, etiqueta_binaria
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/ML_antivirus_kaspersky.csv — 115.15 MB, filas: 589884, formato: csv
  - columnas (muestra): @timestamp, host.ip, host.hostname, rule.name, rule.category, rule.description, file.path, file.hash.md5, file.hash.sha256, danger.type, virus.name, event.reason
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/ML_event_windows_server_correo_interno.csv — 1.27 MB, filas: 5207, formato: csv
  - columnas (muestra): @timestamp, agent.name, data_stream.namespace, event.category, related.user, winlog.api, winlog.event_data.AuthenticationPackageName, winlog.event_data.LogonProcessName, winlog.event_data.LogonType, event_critical.event_id, event_critical.description, host.os.platform, log.level, winlog.event_data.ObjectType, winlog.event_data.ObjectName, winlog.event_data.AccessListDescription, winlog.provider_name, data_stream.dataset, event.action, winlog.channel
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/ML_event_windows_estaciones.csv — 60.89 MB, filas: 201000, formato: csv
  - columnas (muestra): @timestamp, agent.name, data_stream.namespace, event.category, related.user, winlog.api, winlog.event_data.AuthenticationPackageName, winlog.event_data.LogonProcessName, winlog.event_data.LogonType, event_critical.event_id, event_critical.description, host.os.platform, log.level, winlog.event_data.ObjectType, winlog.event_data.ObjectName, winlog.event_data.AccessListDescription, winlog.provider_name, data_stream.dataset, event.action, winlog.channel
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/ML_antimalware.csv — 1.16 MB, filas: 5582, formato: csv
  - columnas (muestra): @timestamp, file.name, file.extension, file.hash.md5, file.hash.sha1, file.hash.sha256, risk.calculated_level, syslog.type, url.original, network.protocol
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/logs_unificados_limpios.csv — 72.94 MB, filas: 856808, formato: csv
  - columnas (muestra): @timestamp, host.ip, rule.name, rule.category, rule.description, file.path, file.hash.md5, file.hash.sha256, virus.name, danger.type, source, hour, dayofweek, month, year
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/mapeo_danger_type_to_attack.csv — 376.00 B, filas: 10, formato: csv
  - columnas (muestra): danger.type, technique_id, tactic
- /Users/alonso/Downloads/Tesis_SIEM_ML/data/raw/ML_WAF.csv — 10.68 MB, filas: 48850, formato: csv
  - columnas (muestra): @timestamp, source.ip, network.protocol, destination.domain, event.id, http.request.method, url.original, destination.port, http.request.bytes, rule.category
