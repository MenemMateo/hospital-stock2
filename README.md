# 🏥 Hospital Stock

¡Bienvenido a **Hospital Stock**! Una aplicación web premium e inteligente para la administración y control de inventarios de medicamentos e insumos médicos, diseñada especialmente para hospitales y ambulancias/móviles de emergencia.

El sistema ofrece una experiencia visual moderna, sofisticada e interactiva con efectos de **Glassmorphism**, diseño totalmente responsivo, micro-animaciones dinámicas y notificaciones inteligentes de alertas.

---

## ✨ Características Principales

### 📊 Dashboard Inteligente
- Visualización en tiempo real del estado de stock de todos los móviles (OK, Alerta de vencimiento o stock bajo, Insumos Vencidos).
- Indicador del total de gastos mensuales acumulados contra un límite configurado dinámicamente, con alertas visuales de advertencia (color rojo sofisticado y accesible).
- Gráficos integrados con **Chart.js** para el análisis de consumos mensuales por móvil.

### 💊 Gestión de Inventario
- Control exacto de medicamentos, precios unitarios, cantidades y fechas de vencimiento.
- Separación automatizada de medicamentos **recuperados** y descartados por **vencimiento**.
- Alertas inteligentes y códigos de colores para insumos próximos a vencer o con stock por debajo del límite mínimo.

### 📝 Registro Cronológico de Movimientos
- Registro de auditoría automática para todas las transacciones del sistema (entradas, salidas, ajustes y recuperaciones).
- **Asociación de Usuario**: Ahora todos los movimientos registran automáticamente qué usuario (médico, enfermero o administrador) realizó la acción para máxima trazabilidad.

### 👤 Perfiles de Usuario Premium
- Tarjeta de perfil interactiva y moderna.
- Carga y actualización de foto de perfil (avatar redondo en la barra de navegación superior).
- Campos de información personal: Nombre completo, biografía, teléfono, dirección y fecha de nacimiento.
- **Acceso Administrativo**: Los superusuarios pueden entrar directamente a visualizar y administrar el perfil de cualquier otro usuario registrado desde el listado administrativo.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3 con Django 6.0
- **Frontend**: HTML5, Vanilla CSS3 (diseño e interactividad customizada), Bootstrap 5.3 (estructura), FontAwesome 6.4 (iconos)
- **Base de Datos**: SQLite3 (desarrollo y almacenamiento rápido)
- **Visualización**: Chart.js (gráficos interactivos integrados con soporte de localización regional)
- **Procesamiento de Imágenes**: Pillow (gestión de subida de fotos de perfil)

---

## 🚀 Instalación y Configuración

Sigue estos pasos sencillos para instalar y correr el proyecto localmente en tu computadora:

### 1. Clonar el repositorio
```bash
git clone https://github.com/MenemMateo/hospital-stock2.git
cd hospital-stock2
```

### 2. Configurar el Entorno Virtual (Opcional si usas el Runner)
Si deseas configurarlo manualmente:
```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Activar en Windows (CMD)
.venv\Scripts\activate.bat

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Correr Migraciones de Base de Datos
```bash
python hospital_stock/manage.py migrate
```

---

## ⚡ Ejecución Rápida en un Clic (Windows)

Para facilitar el inicio inmediato del servidor sin necesidad de escribir comandos en la terminal, hemos incluido un script iniciador rápido:

1. Simplemente haz doble clic sobre el archivo **`iniciar_proyecto.bat`** en la carpeta raíz del proyecto.
2. Este script activará automáticamente el entorno virtual local, verificará que el servidor no tenga problemas y levantará el proyecto de inmediato en:
   👉 **`http://127.0.0.1:8000/`**

---

## 🔒 Usuarios y Roles

La plataforma soporta tres niveles de acceso/roles que restringen dinámicamente las acciones del frontend y del backend:

1. **Superusuario (Administrador)**: Acceso a la base de datos interna, control total del inventario, configuración de límites mensuales de gastos de todo el hospital, creación y eliminación de cuentas, y visualización de perfiles de otros usuarios.
2. **Empleado (Médico/Enfermero)**: Carga y transferencia de insumos a móviles, descartes de insumos vencidos, y ajustes de inventarios.
3. **Espectador (Auditor/Director)**: Visualización de dashboards, inventarios, vencidos, gráficos de gastos y reportes de auditoría en modo de **solo lectura**.

### Crear un nuevo Administrador
Para crear la cuenta de administrador inicial del sistema, corre en la consola:
```bash
python hospital_stock/manage.py createsuperuser
```
Ingresa el nombre de usuario, correo y contraseña deseada para acceder al panel administrativo.
