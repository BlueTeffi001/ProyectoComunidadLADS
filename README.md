# LADS Community App

Aplicación web para la comunidad hispanohablante del juego Love and Deepspace.

## Descripción

Sistema compuesto por un CMS headless (Wagtail) y un frontend (Next.js), diseñado para servir como hub central de la comunidad con guías, lore, herramientas interactivas y gestión de actividades.

## Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Backend | Python, Django, Wagtail |
| Frontend | Next.js 16+, React, TypeScript |
| Base de Datos | PostgreSQL |
| Cache | Redis |
| Almacenamiento | Cloudflare R2 |
| Despliegue | Docker, Dokploy |

## Documentación

La documentación del proyecto se encuentra en el directorio `docs/`:

| Documento | Descripción |
|-----------|-------------|
| [requirements.md](docs/requirements.md) | Especificación de requisitos funcionales y no funcionales |
| [design.md](docs/design.md) | Arquitectura del sistema, modelos de datos y APIs |
| [implementation-plan.md](docs/implementation-plan.md) | Plan de desarrollo con fases, tareas y estimaciones |

## Estructura del Proyecto

```
lads/
├── docs/
│   ├── requirements.md
│   ├── design.md
│   └── implementation-plan.md
├── frontend/          # Next.js
├── backend/           # Wagtail
└── README.md
```

## Funcionalidades Principales

- Sistema de autenticación con verificación por email
- Gestión de usuarios con flujo de aprobación
- CMS para contenido público y exclusivo
- Sistema de comentarios con threads y reacciones
- Calculadoras de recursos del juego
- Calendario de eventos y cumpleaños
- Directorio de miembros

## Roles de Usuario

- Visitante
- Miembro Pendiente
- Miembro Confirmado
- Moderador
- Editor
- Administrador

## Requisitos

- Node.js 20+
- Python 3.12+
- PostgreSQL 16+
- Redis 7+

## Configuración

Consultar la sección de despliegue en [design.md](docs/design.md) para la configuración de servicios y variables de entorno.

## Licencia

Proyecto privado. Todos los derechos reservados.
