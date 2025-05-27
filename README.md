# Musicdibs 🎶

**Proyecto final de ciclo de Desarrollo de Aplicacionees Web.**
Una aplicación que facilita la creación de canciones y el registro de la propiedad intelectual de músicos y cantautores.

## ✨ Funcionalidades

- Verificación de archivos para comprobar si ya han sido certificados
- Registro de usuarios: usuario estándar y administrador

### Funcionalidades para usuarios simples

- Verificación de identidad para permitir registros válidos legalmente
- Creación de proyectos musicales para almacenar la información de cada obra
- Listado de proyectos propios
- Subida de archivos para su certificación
- Generación de archivos textuales con ayuda de IA (letras, partituras, etc.)
- Registro de archivos en blockchain
- Generación de certificados de registro

### Funcionalidades para usuarios administradores

- Gestión de usuarios estándar y visualización básica de sus proyectos
- Asignación de créditos a usuarios
- Cambio de rol entre usuario y administrador
- Eliminación de cuentas de usuario

## 🧱 Arquitectura

La aplicación está dividida en un _frontend_ y un _backend_ , y una base de datos que los respalda. El _backend_ expone toda la de la funcionalidad mediante _endpoints_ específicos, y se conecta con servicios externos de blockchain e IA generativa.

## 🚧 Desarrollo

### Base de datos

La base de datos ha sido implementada con MySQL y está desplegada en Google Cloud.

- Para volver a desplegarla, ejecutar el archivo: `setup_db.sh`.

Para un entorno local, puedes:

- Adaptar el archivo eliminando el uso del proxy de Cloud SQL Auth o,
- Ejecutar los archivos `schema.sql`, `users.sql` que se encuentran en la carpeta `init` y `dev_data.sql` en la carpeta de `seeds`.

### Frontend

Desarrollado en JavaScript usando Vue 3.5.13.

Para ejecutarlo en local, desde la carpeta frontend:

1. Instalar dependencias con
   ```bash
   npm install
   ```
2. Ejecutar el servidor de desarrollo con
   ```bash
   npm run dev
   ```

### Backend

Desarrollado en Python 3.13 con FastAPI 0.115.12.

Documentación de la API

- Swagger: [https://musicdibs.xyz/docs]
- Redoc: [https://musicdibs.xyz/redoc].

Para ejecutarlo en local:

1. Comenta temporalmente las líneas que sirven contenido estático en main.py (línea 56).
2. Activa el entorno virtual:

```bash
   source venv/bin/activate
```

3. Ejecuta el servidor:

```bash
    uvicorn app.main:app --reload
```

> ⚠️ **Importante**: Asegúrate de descomentar las líneas en `main.py` antes de hacer _commit_ a la rama `main`, para evitar errores de despliegue.

## 🚀 Despliegue

Musicdibs está desplegada en un contenedor de **Cloud Run** (Google Cloud), con integración de despliegue continuo desde este repositorio.

Cualquier cambio enviado a la rama `main` activa automáticamente una nueva compilación y despliegue en Cloud Run.
