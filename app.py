from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "recovery_documents.db"

app = Flask(__name__)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entrega (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    documento TEXT NOT NULL,
    fecha_entrega DATE NOT NULL
);
"""

SEED_SQL = """
INSERT INTO entrega (documento, fecha_entrega) VALUES
('CC-1001', '2025-01-05'),
('PAS-2201', '2025-01-14'),
('TI-7634', '2025-02-10'),
('CC-1002', '2025-02-18'),
('CE-8820', '2025-03-03');
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database() -> None:
    with get_connection() as conn:
        conn.executescript(SCHEMA_SQL)
        current_rows = conn.execute("SELECT COUNT(*) AS total FROM entrega").fetchone()["total"]
        if current_rows == 0:
            conn.executescript(SEED_SQL)


def documentos_entregados(fecha_inicio: str, fecha_fin: str) -> int:
    with get_connection() as conn:
        query = """
            SELECT COUNT(*) AS cantidad
            FROM entrega
            WHERE fecha_entrega BETWEEN ? AND ?
        """
        row = conn.execute(query, (fecha_inicio, fecha_fin)).fetchone()
        return int(row["cantidad"])


@app.route("/", methods=["GET", "POST"])
def home():
    resultado = None
    error = None
    fecha_inicio = ""
    fecha_fin = ""

    if request.method == "POST":
        fecha_inicio = request.form.get("fecha_inicio", "")
        fecha_fin = request.form.get("fecha_fin", "")

        try:
            inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fin = datetime.strptime(fecha_fin, "%Y-%m-%d")

            if inicio > fin:
                error = "La fecha inicial no puede ser mayor que la fecha final."
            else:
                resultado = documentos_entregados(fecha_inicio, fecha_fin)
        except ValueError:
            error = "Debes ingresar fechas válidas en formato YYYY-MM-DD."

    return render_template(
        "index.html",
        resultado=resultado,
        error=error,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


if __name__ == "__main__":
    init_database()
    app.run(debug=True)
