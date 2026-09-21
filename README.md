# Recovery Documents

Demostración funcional de una **función SQL almacenada** que cuenta cuántos
documentos fueron entregados entre dos fechas.

El ejercicio académico pedía escribir la función en MySQL. Este repositorio va un
paso más allá: además del script SQL, incluye una aplicación web en Flask que
ejecuta la misma lógica y deja **probarla desde el navegador**, sin instalar un
servidor de base de datos.

> Proyecto de Seminario TICS · Jeferson Wilderman González Tenjo

---

## La función

```sql
DELIMITER $$
CREATE FUNCTION DocumentosEntregados(fecha_inicio DATE, fecha_fin DATE)
RETURNS INT DETERMINISTIC
BEGIN
    DECLARE cantidad INT;

    SELECT COUNT(*) INTO cantidad
    FROM entrega
    WHERE Fecha_entrega BETWEEN fecha_inicio AND fecha_fin;

    RETURN cantidad;
END$$
DELIMITER ;
```

Se usa así:

```sql
SELECT DocumentosEntregados('2023-01-01', '2023-12-31') AS Entregados;
```

Está declarada `DETERMINISTIC` porque con los mismos argumentos y los mismos datos
siempre devuelve lo mismo, lo que permite a MySQL optimizar su ejecución.

## Por qué la app usa SQLite y no MySQL

SQLite **no admite funciones almacenadas**: no existe `CREATE FUNCTION`. Así que la
aplicación no la reproduce, la traduce — ejecuta la misma consulta parametrizada
desde Python:

```python
SELECT COUNT(*) AS cantidad
FROM entrega
WHERE fecha_entrega BETWEEN ? AND ?
```

El resultado es idéntico y la ventaja es práctica: se puede probar el proyecto
clonando y ejecutando, sin levantar un servidor MySQL ni crear un usuario. El
script de MySQL queda en `sql_function_mysql.sql` como el entregable que pedía la
guía.

Los parámetros van con marcadores `?`, nunca concatenados en la cadena, que es lo
que evita la inyección SQL.

## El esquema

```sql
CREATE TABLE IF NOT EXISTS entrega (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    documento      TEXT NOT NULL,
    fecha_entrega  DATE NOT NULL
);
```

La base se crea sola en el primer arranque y se siembra con cinco registros de
ejemplo (`CC-1001`, `PAS-2201`, `TI-7634`, `CC-1002`, `CE-8820`), repartidos entre
enero y marzo de 2025 para que el filtro por rango se note al probarlo.

La siembra **solo ocurre si la tabla está vacía**, así que reiniciar la aplicación
no duplica los datos.

## Ejecutar

Requiere Python 3.10 o superior.

```bash
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abre **http://127.0.0.1:5000** e introduce un rango de fechas.

Para comprobar que filtra de verdad:

| Rango | Resultado esperado |
|---|---|
| `2025-01-01` → `2025-03-31` | 5 |
| `2025-01-01` → `2025-01-31` | 2 |
| `2025-02-01` → `2025-02-28` | 2 |
| `2024-01-01` → `2024-12-31` | 0 |

## Validaciones

El formulario no confía en lo que llega:

- Las dos fechas deben venir en formato `YYYY-MM-DD`, y si no, avisa en vez de fallar
- La fecha inicial no puede ser posterior a la final
- El error se muestra en la misma página, conservando lo que el usuario ya había escrito

## Estructura

```
app.py                     aplicación Flask: esquema, siembra, consulta y rutas
sql_function_mysql.sql     la función almacenada de MySQL (el entregable)
templates/index.html       formulario y resultado
static/styles.css          estilos
requirements.txt           una sola dependencia: Flask
FUNCION PROYECTO ... .docx  documento de entrega del curso
```

## Nota sobre el modo de depuración

`app.py` arranca con `debug=True`. Es cómodo mientras se desarrolla —recarga sola y
muestra el error completo en pantalla— pero **no debe usarse en un servidor
accesible desde internet**: el depurador de Werkzeug permite ejecutar código
arbitrario. Para ejecutarlo fuera de tu equipo, cambia esa línea a `app.run()`.

## Licencia

MIT. Ver [`LICENSE`](LICENSE).
