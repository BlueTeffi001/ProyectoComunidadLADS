# Documento de Requisitos: LADS Community App

## 1. Introducción

LADS Community App es una aplicación web premium para la comunidad hispanohablante del juego "Love and Deepspace". Funciona como hub central para lore, guías de batalla, herramientas interactivas y gestión de actividades comunitarias.

**Arquitectura:** CMS Headless (Wagtail) + Frontend (Next.js)

**Modelo de Despliegue:** Docker vía Dokploy

**Usuarios objetivo:** Comunidad de fans (~1,000 miembros máximo)

---

## 2. Glosario

| Término | Definición |
|---------|------------|
| **Main** | Personaje favorito del juego seleccionado por el miembro |
| **Órbita** | Enemigo o desafío en el sistema de batalla del juego |
| **Protocore** | Recurso/equipo utilizado en batallas |
| **Ascension** | Sistema de mejora de personajes que consume recursos |
| **CMS** | Sistema de gestión de contenido (Wagtail) |
| **Staff** | Roles con permisos elevados: Moderador, Editor, Admin |
| **Stellactrum** | Sistema elemental del juego (6 colores) |
| **Memoria** | Cartas/tarjetas de personaje equipables |

---

## 3. Roles de Usuario

| ID | Rol | Descripción |
|----|-----|-------------|
| ROL-1 | Visitante | Usuario no autenticado |
| ROL-2 | Miembro Pendiente | Autenticado vía OAuth2, esperando aprobación |
| ROL-3 | Miembro Confirmado | Aprobado por admin, acceso completo |
| ROL-4 | Moderador | Modera comentarios y contenido comunitario |
| ROL-5 | Editor | Crea y edita contenido en el CMS |
| ROL-6 | Admin | Control total del sistema |

### Matriz de Permisos

| Permiso | Visitante | Pendiente | Confirmado | Moderador | Editor | Admin |
|---------|:---------:|:---------:|:----------:|:---------:|:------:|:-----:|
| Ver contenido público | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ver contenido exclusivo | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Comentar/Reaccionar | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Editar perfil propio | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Moderar comentarios | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Crear contenido CMS | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Gestionar usuarios | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Aprobar miembros | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 4. Requisitos Funcionales

### REQ-1: Autenticación de Usuarios

**Historia de Usuario:** Como visitante, quiero registrarme e iniciar sesión, para acceder a la comunidad.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

**Registro con Email/Contraseña (Principal):**
1. EL sistema DEBE permitir registro con email y contraseña
2. EL sistema DEBE validar formato de email y fortaleza de contraseña
3. EL sistema DEBE enviar email de verificación antes de activar la cuenta
4. CUANDO el usuario verifica su email, EL sistema DEBE asignar el rol "Miembro Pendiente"

**Proveedores Sociales (Opcional):**
5. EL sistema PUEDE soportar autenticación vía proveedores OAuth2 (Discord, Google, etc.)
6. CUANDO el proveedor autoriza exitosamente, EL sistema DEBE crear o actualizar el usuario local con datos del proveedor

**Sesiones:**
7. EL sistema DEBE generar un JWT válido por 30 días para sesiones
8. SI el token expira, ENTONCES EL sistema DEBE permitir refresh o requerir nuevo login
9. EL sistema DEBE soportar recuperación de contraseña vía email

---

### REQ-2: Flujo de Aprobación de Miembros

**Historia de Usuario:** Como admin, quiero aprobar miembros pendientes, para verificar que pertenecen a la comunidad oficial.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL sistema DEBE mostrar lista de miembros pendientes en panel de admin
2. CUANDO admin aprueba un miembro, EL sistema DEBE cambiar su rol a "Miembro Confirmado"
3. CUANDO admin rechaza un miembro, EL sistema DEBE:
   - Notificar al usuario del rechazo
   - Mostrar la razón del rechazo (campo obligatorio para el admin)
   - Mantener la cuenta en estado "Rechazado" (no eliminar)
4. EL sistema DEBE enviar notificación al usuario cuando su estado cambie (canal por definir)
5. EL sistema DEBE mostrar banner "Cuenta pendiente de aprobación" a miembros pendientes

---

### REQ-3: Experiencia de Miembro Pendiente

**Historia de Usuario:** Como miembro pendiente, quiero saber mi estado y poder navegar contenido público, mientras espero aprobación.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL layout DEBE mostrar banner persistente indicando "Cuenta pendiente de aprobación"
2. EL miembro pendiente PUEDE ver todo el contenido público (guías, lore, calculadoras)
3. CUANDO intenta acceder a contenido exclusivo, EL sistema DEBE mostrar pantalla de "Esperando aprobación"
4. CUANDO intenta comentar o reaccionar, EL sistema DEBE mostrar mensaje indicando que requiere aprobación

---

### REQ-4: Perfil de Miembro

**Historia de Usuario:** Como miembro confirmado, quiero editar mi perfil, para que la comunidad conozca mi personaje favorito y pueda felicitarme en mi cumpleaños.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL sistema DEBE permitir editar los siguientes campos:
   - Foto de perfil (opcional, con placeholder por defecto)
   - Nombre de usuario (obligatorio)
   - Main/Personaje favorito (obligatorio, selección de lista)
   - Fecha de cumpleaños (obligatoria)
   - Descripción corta (opcional)
2. EL sistema DEBE validar que el "Main" sea uno de los 5 personajes válidos
3. EL sistema DEBE mostrar vista previa de cambios antes de guardar
4. CUANDO admin/mod deshabilita edición de perfil, EL miembro NO PUEDE modificar sus datos

---

### REQ-5: Gestión de Personajes (Mains)

**Historia de Usuario:** Como admin, quiero gestionar la lista de personajes disponibles, para agregar nuevos cuando el juego los lance.

**Prioridad:** Deseable

#### Criterios de Aceptación

1. EL sistema DEBE almacenar personajes como entidades en base de datos
2. EL admin PUEDE crear, editar y desactivar personajes desde el CMS
3. Personajes iniciales: Xavier, Sylus, Zayne, Rafayel, Caleb
4. EL sistema DEBE soportar campos: nombre, imagen, descripción

---

### REQ-6: Contenido Público (CMS)

**Historia de Usuario:** Como editor, quiero crear y publicar guías y contenido de lore, para que la comunidad tenga recursos útiles.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL CMS DEBE soportar los siguientes tipos de contenido:
   - Páginas de historia principal
   - Perfiles de personajes
   - Guías de batalla (Órbitas, Protocores)
   - Mitos y Anécdotas
2. EL contenido DEBE soportar texto enriquecido, imágenes y videos embebidos
3. EL contenido público DEBE ser visible para todos (incluyendo visitantes)
4. EL sistema DEBE soportar borrador/publicado como estados de contenido

---

### REQ-7: Contenido Exclusivo (Actividades)

**Historia de Usuario:** Como editor, quiero crear actividades exclusivas para miembros, que contengan información sensible de la comunidad.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL sistema DEBE permitir marcar páginas como "exclusivas para miembros"
2. EL contenido exclusivo DEBE ser visible solo para Miembro Confirmado o superior
3. LAS actividades PUEDEN contener: texto, imágenes, enlaces
4. SI visitante o miembro pendiente accede a URL exclusiva, EL sistema DEBE mostrar pantalla de acceso denegado

---

### REQ-8: Sistema de Comentarios

**Historia de Usuario:** Como miembro confirmado, quiero comentar en guías y contenido, para participar en discusiones de la comunidad.

**Prioridad:** Obligatorio

#### Criterios de Aceptación

1. EL sistema DEBE permitir comentarios en tipos de contenido habilitados
2. LOS comentarios DEBEN soportar respuestas anidadas (hilos/threads)
3. LOS miembros PUEDEN reaccionar con emojis a comentarios
4. SOLO miembros confirmados o superior PUEDEN crear comentarios
5. LOS moderadores/admins PUEDEN eliminar comentarios
6. LOS admins PUEDEN deshabilitar comentarios globalmente o por contenido

---

### REQ-9: Calendario de Eventos

**Historia de Usuario:** Como miembro, quiero ver un calendario con cumpleaños y eventos, para participar en actividades de la comunidad.

**Prioridad:** Deseable

#### Criterios de Aceptación

1. EL calendario DEBE mostrar:
   - Cumpleaños de miembros (automático desde perfiles)
   - Actividades/dinámicas de comunidad
   - Eventos del juego (banners, actualizaciones)
2. LOS eventos PUEDEN contener: título, descripción, imágenes, enlaces
3. EL contenido del calendario de cumpleaños DEBE ser exclusivo (solo miembros confirmados)
4. EL staff PUEDE crear/editar eventos desde el CMS

---

### REQ-10: Calculadora de Ascensión

**Historia de Usuario:** Como jugador, quiero calcular recursos necesarios para subir de nivel mis memorias, para planificar mi progreso.

**Prioridad:** Deseable

#### Criterios de Aceptación

1. LA calculadora DEBE aceptar:
   - Nivel actual de memoria
   - Nivel objetivo
   - Rareza de memoria
2. LA calculadora DEBE calcular y mostrar:
   - Oro requerido
   - XP requerido
   - Stamina necesaria
   - Cristales necesarios
3. LA calculadora DEBE ser accesible públicamente (sin autenticación)
4. LA calculadora DEBE ser un componente React (lógica en frontend)

#### Datos de Referencia

| Rango de Nivel | Oro Aproximado | Materiales |
|----------------|----------------|------------|
| 1-10 | ~2,000 | - |
| 10-20 | ~5,000 | 10x N-Cristales |
| 20-30 | ~10,000 | 15x N-Cristales |
| 30-40 | ~20,000 | 10x R-Cristales |
| 40-50 | ~40,000 | 15x R-Cristales |
| 50-60 | ~80,000 | 20x SR-Cristales |
| 60-70 | ~150,000 | 10x SSR-Cristales |
| 70-80 | ~300,000 | 20x SSR-Cristales + Awakening Heart |

**Total aproximado para Max (Nivel 80):** ~600,000 Oro, ~3,000 Energía (~2 semanas)

---

### REQ-11: Directorio de Miembros

**Historia de Usuario:** Como miembro, quiero ver el directorio de miembros, para conocer a otros fans y sus personajes favoritos.

**Prioridad:** Deseable

#### Criterios de Aceptación

1. EL directorio DEBE mostrar lista de miembros confirmados
2. EL directorio DEBE mostrar: foto, nombre, main
3. EL directorio DEBE permitir filtrar por personaje favorito (main)
4. EL directorio DEBE ser exclusivo para miembros confirmados

---

### REQ-12: Sistema de Notificaciones

**Historia de Usuario:** Como miembro, quiero recibir notificaciones de eventos importantes, para no perderme actividades de la comunidad.

**Prioridad:** Opcional

#### Criterios de Aceptación

1. EL sistema DEBE tener arquitectura agnóstica al canal de notificación
2. EL sistema DEBE soportar al menos uno de: Discord, Email, WhatsApp, Telegram
3. LAS notificaciones DEBEN incluir: aprobación de cuenta, nuevos eventos, respuestas a comentarios
4. LOS miembros PUEDEN configurar sus preferencias de notificación

---

### REQ-13: Calculadora de Daño (Futuro)

**Historia de Usuario:** Como jugador avanzado, quiero simular el daño de mis builds, para optimizar mis Protocores.

**Prioridad:** Opcional (Fase 2)

#### Criterios de Aceptación

1. LA calculadora DEBE soportar selección de personaje y companion (Lightseeker, Foreseer, etc.)
2. LA calculadora DEBE aplicar escalado correcto:
   - Xavier/Rafayel/Sylus: Escalan con ATK
   - Zayne (Foreseer): Escala con DEF
3. LA calculadora DEBE calcular multiplicadores de:
   - Crítico: `1 + (TasaCrit × DañoCrit)`
   - Debilidad: Bonus de daño a enemigos debilitados
   - Elemental: Bonus por Stellactrum coincidente
4. LA calculadora DEBE mostrar DPS estimado y daño por golpe crítico

---

## 5. Requisitos No Funcionales

### RNF-1: Rendimiento

- EL sistema DEBE cargar páginas en menos de 3 segundos (LCP)
- EL sistema DEBE soportar 1,000 usuarios registrados
- LA API DEBE responder en menos de 500ms para operaciones comunes

### RNF-2: Seguridad

- EL sistema DEBE autenticar mediante OAuth2 + JWT
- EL sistema DEBE validar permisos en cada petición a contenido exclusivo
- EL sistema DEBE sanitizar todo input de usuario (prevención XSS/SQL injection)

### RNF-3: Disponibilidad

- EL sistema DEBE estar disponible 99% del tiempo
- EL sistema DEBE implementar respaldos automáticos de base de datos

### RNF-4: Mantenibilidad

- EL código DEBE seguir estándares de linting (ESLint, Black/Ruff)
- EL sistema DEBE usar Docker para despliegue reproducible

---

## 6. Restricciones

### Técnicas
- Backend CMS: Wagtail (Python/Django)
- Frontend: Next.js (React)
- Base de Datos: PostgreSQL
- Despliegue: Docker vía Dokploy
- Idioma: Solo español (sin internacionalización)

### De Negocio
- Usuarios máximos: 1,000 miembros
- Presupuesto: Hosting gratuito/económico
- Timeline: Por definir

---

## 7. Fuera de Alcance (v1.0)

- [ ] Integración con Planka u otro Kanban externo
- [ ] SSO con herramientas externas
- [ ] Múltiples idiomas
- [ ] Aplicación móvil nativa
- [ ] Coeficientes de calculadora gestionables desde CMS
- [ ] Calculadora de daño avanzada (diferida a Fase 2)

---

## 8. Decisiones Tomadas

| ID | Pregunta | Decisión |
|----|----------|----------|
| D1 | Duración del JWT | 30 días |
| D2 | Rechazo de miembros | Se notifica con razón, cuenta no se elimina |
| D3 | Personajes iniciales | 5: Xavier, Sylus, Zayne, Rafayel, Caleb |
| D4 | Fecha cumpleaños | Obligatoria en perfil |

---

## 9. Preguntas Abiertas

| ID | Pregunta | Estado |
|----|----------|--------|
| Q1 | ¿Qué canal de notificación se implementa primero? | Pendiente |
| Q2 | ¿Campos adicionales de perfil por definir? | Pendiente |
| Q3 | ¿Kanban custom o alternativa integrable? | Por investigar |
