from flask import Flask, render_template, request, redirect, url_for, send_file, session
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave-segura"

# --- BASE DE DATOS ---
def conectar_db():
    ruta = os.path.join(os.path.dirname(__file__), "reservas.db")
    return sqlite3.connect(ruta)

def inicializar_bd():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insertar_reserva(nombre, fecha, hora):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reservas (nombre, fecha, hora) VALUES (?, ?, ?)", (nombre, fecha, hora))
    conn.commit()
    conn.close()

def obtener_reservas(filtro_nombre=None, filtro_fecha=None):
    conn = conectar_db()
    cursor = conn.cursor()
    consulta = "SELECT * FROM reservas WHERE 1=1"
    parametros = []

    if filtro_nombre:
        consulta += " AND nombre LIKE ?"
        parametros.append(f"%{filtro_nombre}%")
    if filtro_fecha:
        consulta += " AND fecha = ?"
        parametros.append(filtro_fecha)

    consulta += " ORDER BY fecha, hora"
    cursor.execute(consulta, parametros)
    reservas = cursor.fetchall()
    conn.close()
    return reservas

def eliminar_reserva(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# --- RUTA INICIO ---
@app.route("/")
def inicio():
    return render_template("inicio.html")

# --- RUTA RESERVAS ---
@app.route("/reservas", methods=["GET", "POST"])
def reservas():
    error = None
    ahora = datetime.now()

    if request.method == "POST":
        nombre = request.form.get("nombre")
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")

        if not nombre or not fecha or not hora:
            error = "Todos los campos son obligatorios."
        else:
            try:
                hora_split = hora.split(":")
                hora_int = int(hora_split[0])
                minuto_int = int(hora_split[1]) if len(hora_split) > 1 else 0

                if (
                    datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M") < ahora
                    or hora_int < 7
                    or (hora_int > 12 and hora_int < 16)
                    or (hora_int == 12 and minuto_int > 0)
                    or hora_int > 21
                    or (hora_int == 21 and minuto_int > 0)
                ):
                    error = "Horario no permitido o fecha pasada."
                else:
                    insertar_reserva(nombre, fecha, hora)
                    return redirect(url_for("reservas"))
            except ValueError:
                error = "Formato de hora inválido. Usa HH:MM."

    filtro_nombre = request.args.get("nombre_busqueda")
    filtro_fecha = request.args.get("fecha_busqueda")
    reservas_lista = obtener_reservas(filtro_nombre, filtro_fecha)

    return render_template("index.html", reservas=reservas_lista, error=error, ahora=ahora)

@app.route("/cancelar/<int:id>")
def cancelar(id):
    # Solo permite cancelar reservas futuras
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, hora FROM reservas WHERE id = ?", (id,))
    reserva = cursor.fetchone()
    conn.close()

    if reserva:
        fecha_hora = f"{reserva[0]} {reserva[1]}"
        if datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M") >= datetime.now():
            eliminar_reserva(id)

    return redirect(url_for("reservas"))



# --- RUTA ELIMINAR ---
@app.route("/eliminar/<int:id>")
def eliminar(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    eliminar_reserva(id)
    return redirect(url_for("reservas"))

# --- RUTA DESCARGAR ---
@app.route("/descargar")
def descargar():
    if not session.get("admin"):
        return redirect(url_for("login"))

    import csv
    ruta_csv = "reservas.csv"
    reservas = obtener_reservas()

    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Fecha", "Hora"])
        for r in reservas:
            writer.writerow(r[1:])

    return send_file(ruta_csv, as_attachment=True)

# --- LOGIN ---
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")
        if usuario == "admin" and clave == "admin123":
            session["admin"] = True
            return redirect(url_for("reservas"))
        else:
            error = "Credenciales incorrectas."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))

# --- INICIO APP ---
inicializar_bd()

if __name__ == "__main__":
    app.run(debug=True)