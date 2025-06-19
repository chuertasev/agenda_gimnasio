import sqlite3
import os

ruta = os.path.join(os.path.dirname(__file__), "agenda.db")
conn = sqlite3.connect(ruta)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS turnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    fecha TEXT NOT NULL,
    hora TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Base de datos creada correctamente.")