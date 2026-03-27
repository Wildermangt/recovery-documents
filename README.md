# Recovery Documents App

Aplicación web sencilla para consultar cuántos documentos han sido entregados en un rango de fechas, inspirada en la función SQL del proyecto académico.

## Requisitos

- Python 3.10+
- pip

## Instalación y ejecución

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Luego abre `http://127.0.0.1:5000`.

## ¿Qué incluye?

- Interfaz web para ingresar fecha inicial y final.
- Validación de fechas.
- Consulta a base SQLite (`recovery_documents.db`) para contar entregas.
- Script SQL de MySQL equivalente en `sql_function_mysql.sql`.

## Datos de ejemplo

La app carga automáticamente datos de ejemplo en la tabla `entrega` la primera vez que corre.
