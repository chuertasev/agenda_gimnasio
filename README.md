# 🥊 Agenda de Clases - Sanctum Box

Este proyecto es un sistema de reservas de clases para el gimnasio **Sanctum Box**, diseñado con una interfaz web moderna, control de acceso para administrador, validaciones de horario y gestión de reservas.

## 🌐 Demo en línea (próximamente en Render)

> Acceso rápido para usuarios y administradores desde la interfaz web.  
> El botón `Ingresar` permite visualizar la agenda de clases.

---

## 🚀 Características principales

- 📅 Agenda de clases personalizadas por día y hora
- 🔐 Panel de administración protegido con login
- 🕓 Validación de horarios disponibles (07:00–12:00 y 16:00–21:00)
- 🔎 Búsqueda de reservas por nombre y/o fecha
- ❌ Cancelación de clases futuras por parte de los usuarios
- 🗑️ Eliminación de reservas por el administrador (pasadas y futuras)
- 📥 Exportación de reservas a CSV (solo administrador)
- 🎨 Estilo visual unificado (paleta corporativa de Sanctum Box)

---

## 🧱 Tecnologías usadas

- **Python 3**
- **Flask** (framework backend)
- **SQLite3** (base de datos liviana)
- **HTML5 + Bootstrap 5** (frontend responsivo)
- **Render.com** (despliegue)

---

## 🗂️ Estructura del proyecto

agenda_gimnasio/
│
├── app.py # Lógica principal de la aplicación
├── crear_db.py # Script opcional para generar la base de datos
├── reservas.db # Base de datos SQLite generada automáticamente
├── requirements.txt # Dependencias para Render
├── render.yaml # Archivo de configuración para despliegue en Render
│
├── templates/ # Archivos HTML
│ ├── index.html # Página principal (agenda de reservas)
│ ├── inicio.html # Página de presentación (pública)
│ ├── login.html # Login de administrador
│ └── eliminar.html # Opción extendida para eliminar como admin (opcional)


---

## 👨‍💻 Cómo usar este proyecto localmente

1. **Clona el repositorio**

git clone https://github.com/chuertasv/agenda_gimnasio.git
cd agenda_gimnasio

Instala Flask
pip install flask

Ejecuta la aplicación
python app.py

Accede desde el navegador
http://127.0.0.1:5000

🔑 Credenciales de prueba (Admin)
Usuario: admin

Clave: admin123
