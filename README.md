# ETL (PDF → Chunks → Embeddings → Qdrant) — Documentación en Español
 [![Release](https://img.shields.io/badge/release-v0.1.0-blue.svg)](https://github.com/21Hell/ETL/releases)

Este repositorio contiene una canalización ETL diseñada para ejecutarse localmente (on‑prem) usando Docker Compose y Apache Airflow. El flujo principal:

- Descargar PDFs (o consumir una librería local)
- Extraer texto y dividir en chunks
- Generar embeddings para cada chunk
- Subir (upsert) los vectores a Qdrant (vector DB)

Objetivo: mantener todos los datos y servicios localmente, sin depender de servicios en la nube.

## Estructura principal

Raíz del proyecto (resumen):

```
ETL/
├─ docker-compose.yml         # Orquestación de servicios (Airflow, Postgres, Redis, Qdrant)
├─ dags/pdf_etl_dag.py        # Definición del DAG de Airflow
├─ config/settings.yaml       # Parámetros (rutas, qdrant, chunking)
├─ src/etl/                   # Código del pipeline (download, chunk, embed, load)
│  ├─ downloader.py
│  ├─ chunker.py
│  ├─ embedder.py
│  ├─ loader_qdrant.py
│  └─ utils.py
├─ src/tools/                 # Scripts y servidores auxiliares (ingest_one, rag_chat, visual_server)
├─ data/                      # Almacenamiento local (raw, chunks, embeddings)
├─ requirements/              # Requisitos pip (airflow, dev)
├─ urls.txt                   # Lista de URLs de ejemplo para descarga
└─ tests/                     # Tests unitarios (pytest)
```

## Requisitos (resumen)

- Docker & Docker Compose (para ejecutar la pila Airflow + Qdrant localmente)
- Python 3.10+ (para desarrollo local / ejecutar scripts fuera de contenedores)
- Las dependencias Python están en `requirements/airflow.txt` y `requirements/dev.txt`.

Nota: Airflow y sus dependencias son pesadas; para desarrollo rápido puede ejecutarse solo los scripts Python sin arrancar los contenedores.

## Cómo ejecutar (opciones)

1) Ejecutar todo con Docker Compose (recomendado para reproducibilidad)

- Precondiciones: Docker y Docker Compose instalados.
- Generar clave Fernet para Airflow y exportarla en `.env` (ver `DOCS.md` para ejemplos).

Ejemplo (bash):

```bash
cd /home/cwolf/Documents/ETL
# inicializar Airflow (configura imágenes/volúmenes)
docker compose up -d airflow-init
# arrancar todos los servicios
docker compose up -d
```

Acceso a UI de Airflow: http://localhost:8080 (credenciales por defecto en la configuración local).

2) Ejecutar partes localmente (sin Docker)

Esto es útil para desarrollo o tests rápidos. Requiere pip packages locales.

Crear y activar entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```

Ejecutar tests unitarios:

```bash
pytest -q
```

Ejecutar un ingreso de archivo único (end-to-end, útil para testear un PDF local):

```bash
python -m src.tools.ingest_one /ruta/a/tu/archivo.pdf --settings config/settings.yaml
```

3) Ejecutar solo servidores de búsqueda / RAG

Si ya tienes embeddings en Qdrant y quieres exponer el chat o visualización:

```bash
python -m uvicorn src.tools.visual_server:app --host 127.0.0.1 --port 5050
python -m uvicorn src.tools.rag_chat:app --host 127.0.0.1 --port 5051
```

## Configuración clave

- `config/settings.yaml`: rutas a `data/raw`, `data/chunks`, `data/embeddings`, y configuración de Qdrant (host/port/collection/vector_size).
- `urls.txt`: lista de URLs a descargar (una por línea, soporta `#` como comentario).

## Desarrollo y pruebas

- Los tests están en `tests/` y usan `pytest`.
- Para depurar partes específicas, ejecuta módulos desde la raíz con `python -m src.tools.ingest_one` o importando funciones desde `src/etl`.

## Notas operativas

- El DAG `pdf_etl_local` (archivo `dags/pdf_etl_dag.py`) define cuatro tareas: download → chunk → embed → load_qdrant.
- Los pasos son idempotentes: si los archivos de salida existen, los pasos se saltan para permitir ejecuciones incrementales.
- `src/etl/embedder.py` usa `fastembed` con el modelo `BAAI/bge-small-en-v1.5` por defecto (384 dimensiones). Cambia el modelo y `config/settings.yaml` si es necesario.

## Ejecución recomendada si falla la instalación local

- Si la instalación de dependencias locales es complicada (Airflow es pesada), arranca la pila con Docker Compose y usa `docker compose exec` para correr scripts dentro de los contenedores.

Ejemplo:

```bash
# Ejecutar ingest_one dentro del contenedor (ajusta nombre a tu despliegue)
docker compose exec airflow-webserver python -m src.tools.ingest_one /opt/airflow/local_library/MiLibro.pdf --settings /opt/airflow/config/settings.yaml
```

## Contacto / próximos pasos

- Para ayudar más, puedo:
	- Generar un `Makefile` o scripts de convenience para arrancar la pila.
	- Añadir un `docs/` con diagramas y ejemplos de `settings.yaml`.
	- Preparar un entorno Docker más ligero para desarrollo (sin Airflow completo).

---

Documentación generada automáticamente: resumen de las rutas y comandos más usados.

