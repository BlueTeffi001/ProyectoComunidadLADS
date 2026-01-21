# Plan de Implementación: LADS Community App

## Límites del Proyecto

### MVP (Fase 1)
- Autenticación email/contraseña
- Sistema de roles y aprobación de miembros
- CMS con contenido público y exclusivo
- Perfiles de usuario con Main
- Sistema de comentarios básico

### Fase 2
- Proveedores OAuth (Discord, Google)
- Calendario de eventos
- Directorio de miembros
- Calculadora de Ascensión

### Fuera de Alcance
- Kanban/gestión de tareas
- Calculadora de daño avanzada
- Aplicación móvil

---

## Fases de Desarrollo

### Fase 1: Infraestructura (Semana 1-2)

**Objetivo:** Establecer base del proyecto y despliegue

#### Tareas

- [ ] 1.1 Configuración del Repositorio
  - Crear estructura de monorepo (`/frontend`, `/backend`)
  - Configurar `.gitignore`, `README.md`
  - Configurar linting (ESLint, Black/Ruff)
  - _Dependencias: Ninguna_
  - _Estimado: 2 horas_

- [ ] 1.2 Backend: Scaffolding Wagtail
  - Inicializar proyecto Django + Wagtail
  - Configurar `settings.py` para producción
  - Configurar conexión PostgreSQL
  - Configurar almacenamiento Cloudflare R2
  - _Requisitos: REQ-6 (CMS)_
  - _Dependencias: 1.1_
  - _Estimado: 4 horas_

- [ ] 1.3 Frontend: Scaffolding Next.js
  - Inicializar proyecto Next.js 16+ con App Router
  - Configurar TypeScript
  - Instalar dependencias base (Tailwind, etc.)
  - _Requisitos: RNF-1 (Rendimiento)_
  - _Dependencias: 1.1_
  - _Estimado: 3 horas_

- [ ] 1.4 Dockerfiles
  - Crear `Dockerfile` para backend
  - Crear `Dockerfile` para frontend
  - Probar build local
  - _Requisitos: RNF-4 (Mantenibilidad)_
  - _Dependencias: 1.2, 1.3_
  - _Estimado: 3 horas_

- [ ] 1.5 Despliegue Inicial en Dokploy
  - Configurar servicios en Dokploy
  - Configurar PostgreSQL y Redis
  - Configurar variables de entorno
  - Verificar acceso a dominio
  - _Dependencias: 1.4_
  - _Estimado: 4 horas_

---

### Fase 2: Autenticación (Semana 2-3)

**Objetivo:** Sistema de usuarios funcional

#### Tareas

- [ ] 2.1 Modelo de Usuario Personalizado
  - Crear `CustomUser` con campos adicionales
  - Agregar campos: `status`, `role`, `birthday`, `bio`
  - Crear migraciones
  - _Requisitos: REQ-1, REQ-4_
  - _Dependencias: 1.2_
  - _Estimado: 3 horas_

- [ ] 2.2 API de Autenticación
  - Implementar registro con email/contraseña
  - Implementar login con JWT
  - Implementar verificación de email
  - Implementar recuperación de contraseña
  - _Requisitos: REQ-1_
  - _Dependencias: 2.1_
  - _Estimado: 8 horas_

- [ ] 2.3 Frontend: Páginas de Auth
  - Crear página `/registro`
  - Crear página `/login`
  - Crear página `/verificar`
  - Crear página `/recuperar-contrasena`
  - Integrar con API
  - _Requisitos: REQ-1_
  - _Dependencias: 2.2_
  - _Estimado: 6 horas_

- [ ] 2.4 Middleware de Autorización
  - Implementar middleware Next.js para rutas protegidas
  - Implementar verificación de estado (pendiente/aprobado)
  - Redirigir según permisos
  - _Requisitos: REQ-3_
  - _Dependencias: 2.3_
  - _Estimado: 4 horas_

---

### Fase 3: Gestión de Usuarios (Semana 3-4)

**Objetivo:** Panel admin y flujo de aprobación

#### Tareas

- [ ] 3.1 Modelo de Personajes
  - Crear modelo `Character` en Wagtail
  - Agregar los 5 personajes iniciales
  - Exponer en API
  - _Requisitos: REQ-5_
  - _Dependencias: 1.2_
  - _Estimado: 2 horas_

- [ ] 3.2 Perfil de Usuario
  - Frontend: crear página `/perfil`
  - Formulario de edición con validación
  - Selector de Main (personaje)
  - Upload de foto de perfil a R2
  - _Requisitos: REQ-4_
  - _Dependencias: 2.3, 3.1_
  - _Estimado: 6 horas_

- [ ] 3.3 Panel de Aprobación (Admin)
  - Crear vista en Wagtail Admin para usuarios pendientes
  - Botones aprobar/rechazar
  - Campo de razón de rechazo
  - API para cambiar estado
  - _Requisitos: REQ-2_
  - _Dependencias: 2.1_
  - _Estimado: 5 horas_

- [ ] 3.4 Notificaciones Email
  - Configurar envío de email (SMTP)
  - Template: verificación de cuenta
  - Template: cuenta aprobada/rechazada
  - _Requisitos: REQ-2, REQ-12_
  - _Dependencias: 3.3_
  - _Estimado: 4 horas_

---

### Fase 4: CMS y Contenido (Semana 4-5)

**Objetivo:** Sistema de contenido funcional

#### Tareas

- [ ] 4.1 Modelos de Páginas Wagtail
  - Crear `ContentPage` con StreamField
  - Agregar campo `is_exclusive`
  - Agregar campo `allow_comments`
  - Configurar tipos de contenido (guía, lore, actividad)
  - _Requisitos: REQ-6, REQ-7_
  - _Dependencias: 1.2_
  - _Estimado: 5 horas_

- [ ] 4.2 API de Contenido
  - Endpoint GET `/api/pages/`
  - Endpoint GET `/api/pages/{slug}`
  - Filtrar contenido exclusivo según permisos
  - _Requisitos: REQ-6, REQ-7_
  - _Dependencias: 4.1_
  - _Estimado: 4 horas_

- [ ] 4.3 Frontend: Renderizado de Contenido
  - Crear componentes para StreamField blocks
  - Página dinámica `/guias/[slug]`
  - Página dinámica `/lore/[slug]`
  - Manejo de contenido exclusivo
  - _Requisitos: REQ-6, REQ-7_
  - _Dependencias: 4.2_
  - _Estimado: 6 horas_

- [ ] 4.4 Páginas de Personajes
  - Crear template de perfil de personaje
  - Listar personajes en `/personajes`
  - Detalle en `/personajes/[slug]`
  - _Requisitos: REQ-6_
  - _Dependencias: 3.1, 4.3_
  - _Estimado: 4 horas_

---

### Fase 5: Comentarios (Semana 5-6)

**Objetivo:** Sistema de interacción comunitaria

#### Tareas

- [ ] 5.1 Modelo de Comentarios
  - Crear modelo `Comment` con threads
  - Crear modelo `Reaction`
  - Migraciones
  - _Requisitos: REQ-8_
  - _Dependencias: 4.1_
  - _Estimado: 3 horas_

- [ ] 5.2 API de Comentarios
  - GET `/api/pages/{id}/comments`
  - POST `/api/pages/{id}/comments`
  - DELETE `/api/comments/{id}`
  - POST/DELETE `/api/comments/{id}/reactions`
  - _Requisitos: REQ-8_
  - _Dependencias: 5.1_
  - _Estimado: 5 horas_

- [ ] 5.3 Frontend: Componente de Comentarios
  - Lista de comentarios con threads
  - Formulario de nuevo comentario
  - Botones de reacciones emoji
  - Botón eliminar (para mods/admins)
  - _Requisitos: REQ-8_
  - _Dependencias: 5.2_
  - _Estimado: 6 horas_

---

### Fase 6: Funcionalidades Adicionales (Semana 6-7)

**Objetivo:** Completar features secundarios

#### Tareas

- [ ] 6.1 Calculadora de Ascensión
  - Crear componente React con lógica de cálculo
  - UI con inputs y resultados
  - Datos de costos hardcodeados
  - _Requisitos: REQ-10_
  - _Dependencias: 1.3_
  - _Estimado: 6 horas_

- [ ] 6.2 Directorio de Miembros
  - API GET `/api/users/` (solo confirmados)
  - Frontend: página `/directorio`
  - Filtro por Main (personaje)
  - _Requisitos: REQ-11_
  - _Dependencias: 3.2_
  - _Estimado: 4 horas_

- [ ] 6.3 Calendario de Eventos
  - Modelo `Event` en backend
  - API de eventos
  - Componente calendario en frontend
  - Mostrar cumpleaños automáticamente
  - _Requisitos: REQ-9_
  - _Dependencias: 3.2_
  - _Estimado: 8 horas_

---

### Fase 7: Testing y Pulido (Semana 7-8)

**Objetivo:** Calidad y preparación para producción

#### Tareas

- [ ] 7.1 Tests Backend
  - Tests unitarios de modelos
  - Tests de API con pytest
  - Cobertura mínima 70%
  - _Requisitos: RNF-4_
  - _Dependencias: Fases 1-6_
  - _Estimado: 8 horas_

- [ ] 7.2 Tests Frontend
  - Tests de componentes con Jest/RTL
  - Tests E2E críticos con Playwright
  - _Requisitos: RNF-4_
  - _Dependencias: Fases 1-6_
  - _Estimado: 6 horas_

- [ ] 7.3 Revisión de Seguridad
  - Validar sanitización de inputs
  - Revisar permisos en todos los endpoints
  - Verificar CORS y headers
  - _Requisitos: RNF-2_
  - _Dependencias: Fases 1-6_
  - _Estimado: 4 horas_

- [ ] 7.4 Optimización de Rendimiento
  - Verificar LCP < 3s
  - Optimizar imágenes
  - Configurar cache headers
  - _Requisitos: RNF-1_
  - _Dependencias: 7.1, 7.2_
  - _Estimado: 4 horas_

- [ ] 7.5 Documentación
  - README con instrucciones de desarrollo
  - Documentación de API (OpenAPI/Swagger)
  - Guía de despliegue
  - _Dependencias: Fases 1-6_
  - _Estimado: 4 horas_

---

## Resumen de Estimaciones

| Fase | Tareas | Horas Estimadas |
|------|--------|-----------------|
| 1. Infraestructura | 5 | 16 |
| 2. Autenticación | 4 | 21 |
| 3. Gestión Usuarios | 4 | 17 |
| 4. CMS y Contenido | 4 | 19 |
| 5. Comentarios | 3 | 14 |
| 6. Funcionalidades | 3 | 18 |
| 7. Testing y Pulido | 5 | 26 |
| **Total** | **28** | **~131 horas** |

**Estimación de Timeline:** 7-8 semanas (considerando ~20 horas/semana de desarrollo)

---

## Plan de Verificación

### Tests Automatizados

| Tipo | Herramienta | Comando |
|------|-------------|---------|
| Backend Unit | pytest | `cd backend && pytest` |
| Backend Coverage | pytest-cov | `cd backend && pytest --cov=.` |
| Frontend Unit | Jest | `cd frontend && npm test` |
| Frontend E2E | Playwright | `cd frontend && npx playwright test` |

### Tests Manuales Críticos

| Flujo | Pasos |
|-------|-------|
| **Registro** | 1. Ir a `/registro` → 2. Completar formulario → 3. Verificar email recibido → 4. Click en link → 5. Confirmar estado "pendiente" en perfil |
| **Aprobación** | 1. Login como admin → 2. Ir a `/admin` → 3. Ver usuario pendiente → 4. Aprobar → 5. Verificar email enviado → 6. Usuario puede acceder a exclusivo |
| **Contenido Exclusivo** | 1. Crear página exclusiva en CMS → 2. Acceder como visitante → 3. Debe mostrar bloqueo → 4. Acceder como miembro aprobado → 5. Debe mostrar contenido |
| **Comentarios** | 1. Login como miembro → 2. Ir a guía → 3. Escribir comentario → 4. Agregar reacción → 5. Verificar persistencia |

---

## Notas de Implementación

> **Patrón de desarrollo recomendado:** Vertical slice
> - Completar un flujo completo (backend + frontend) antes de pasar al siguiente
> - Facilita testing temprano y feedback continuo

> **Prioridad de errores:**
> 1. Seguridad (auth, permisos)
> 2. Funcionalidad core (registro, contenido)
> 3. UX y pulido
