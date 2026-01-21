# Documento de Diseño: LADS Community App

## 1. Visión General

Sistema web headless compuesto por un CMS backend (Wagtail/Django) y un frontend (Next.js), desplegados en una VPS mediante Dokploy con Docker Compose.

**Principios de Diseño:**
- Separación clara entre CMS y frontend
- API REST para comunicación entre sistemas
- Autenticación centralizada en el backend
- Frontend como consumidor de contenido

---

## 2. Arquitectura del Sistema

### 2.1 Diagrama de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VPS (Dokploy)                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐           │
│  │   Traefik   │────▶│   Next.js   │     │   Wagtail   │           │
│  │   (Proxy)   │     │  (Frontend) │     │   (CMS)     │           │
│  └─────────────┘     └──────┬──────┘     └──────┬──────┘           │
│         │                   │                   │                   │
│         │                   │    API REST       │                   │
│         │                   └───────────────────┘                   │
│         │                                                           │
│         │                   ┌─────────────┐                         │
│         │                   │  PostgreSQL │                         │
│         │                   │    (DB)     │                         │
│         │                   └─────────────┘                         │
│         │                                                           │
│         │                   ┌─────────────┐                         │
│         └──────────────────▶│    Redis    │ (Sesiones/Cache)       │
│                             └─────────────┘                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Mapa de Componentes

| ID | Componente | Tipo | Responsabilidad | Puerto |
|----|------------|------|-----------------|--------|
| COMP-1 | Traefik | Proxy Reverso | Enrutamiento, SSL, Load Balancing | 80, 443 |
| COMP-2 | Next.js | Frontend | UI, SSR, Calculadoras | 3000 |
| COMP-3 | Wagtail | Backend CMS | Gestión contenido, API, Auth | 8000 |
| COMP-4 | PostgreSQL | Base de Datos | Persistencia | 5432 |
| COMP-5 | Redis | Cache/Sesiones | Cache de API, sesiones JWT | 6379 |

---

## 3. Flujos de Datos

### 3.1 Flujo de Autenticación (Email/Contraseña)

```
1. Usuario → Next.js: Envía credenciales (email, contraseña)
2. Next.js → Wagtail API: POST /api/auth/login
3. Wagtail → PostgreSQL: Valida credenciales
4. Wagtail → Next.js: Retorna JWT + refresh token
5. Next.js → Usuario: Almacena tokens (httpOnly cookies)
6. Next.js → Wagtail: Requests con header Authorization: Bearer {JWT}
```

### 3.2 Flujo de Aprobación de Miembros

```
1. Usuario se registra → Estado: "pendiente"
2. Admin accede a Wagtail Admin → Ve lista de pendientes
3. Admin aprueba/rechaza → PATCH /api/users/{id}/status
4. Sistema → Notificación al usuario (email/webhook)
5. Usuario → Ahora tiene acceso a contenido exclusivo
```

### 3.3 Flujo de Contenido CMS

```
1. Editor → Wagtail Admin: Crea/edita página
2. Editor → Marca como "público" o "exclusivo"
3. Editor → Publica
4. Next.js → GET /api/pages/{slug}
5. Next.js → Verifica permisos del usuario
6. Next.js → Renderiza contenido (si autorizado)
```

---

## 4. Modelos de Datos

### 4.1 Usuario (CustomUser)

```python
class CustomUser(AbstractUser):
    # Heredado: username, email, password, first_name, last_name
    
    # Campos personalizados
    discord_id: str | None        # Si usa OAuth Discord
    avatar: ImageField | None     # Foto de perfil
    birthday: DateField           # Cumpleaños (obligatorio)
    bio: TextField | None         # Descripción corta
    main: ForeignKey[Character]   # Personaje favorito (obligatorio)
    
    # Estado y roles
    status: str                   # 'pending', 'approved', 'rejected'
    rejection_reason: str | None  # Razón si fue rechazado
    role: str                     # 'member', 'moderator', 'editor', 'admin'
    
    # Control
    can_edit_profile: bool = True
    can_comment: bool = True
    
    # Timestamps
    created_at: DateTimeField
    approved_at: DateTimeField | None
    approved_by: ForeignKey[CustomUser] | None
```

### 4.2 Personaje (Character)

```python
class Character(models.Model):
    name: str                     # Xavier, Sylus, Zayne, Rafayel, Caleb
    slug: str                     # URL amigable
    description: TextField
    image: ImageField
    color: str                    # Color temático (hex)
    is_active: bool = True
    
    # Se modelan como relación separada si se necesita
```

### 4.3 Página de Contenido (ContentPage)

```python
class ContentPage(Page):  # Hereda de Wagtail Page
    # Heredado: title, slug, live, first_published_at
    
    # Campos de contenido
    body: StreamField             # Bloques de contenido rico
    featured_image: ImageField | None
    
    # Control de acceso
    is_exclusive: bool = False    # Solo miembros confirmados
    allow_comments: bool = True
    
    # Tipo de contenido
    content_type: str             # 'guide', 'lore', 'activity', 'character'
    
    # SEO
    meta_description: str | None
```

### 4.4 Comentario (Comment)

```python
class Comment(models.Model):
    page: ForeignKey[ContentPage]
    author: ForeignKey[CustomUser]
    parent: ForeignKey['Comment'] | None  # Para threads
    
    content: TextField
    created_at: DateTimeField
    updated_at: DateTimeField
    
    is_deleted: bool = False      # Soft delete
    deleted_by: ForeignKey[CustomUser] | None
```

### 4.5 Reacción (Reaction)

```python
class Reaction(models.Model):
    comment: ForeignKey[Comment]
    user: ForeignKey[CustomUser]
    emoji: str                    # Código emoji unicode
    created_at: DateTimeField
    
    class Meta:
        unique_together = ['comment', 'user', 'emoji']
```

### 4.6 Evento (Event)

```python
class Event(models.Model):
    title: str
    description: TextField
    image: ImageField | None
    link: URLField | None
    
    event_type: str               # 'birthday', 'activity', 'game_event'
    date: DateField
    end_date: DateField | None    # Para eventos de varios días
    
    # Si es cumpleaños, referencia al usuario
    user: ForeignKey[CustomUser] | None
    
    is_exclusive: bool = True     # Por defecto exclusivo
    created_by: ForeignKey[CustomUser]
```

### 4.7 Diagrama de Relaciones

```
┌──────────────┐       ┌──────────────┐
│  CustomUser  │───────│  Character   │
│              │ main  │              │
└──────┬───────┘       └──────────────┘
       │
       │ author
       ▼
┌──────────────┐       ┌──────────────┐
│   Comment    │───────│ ContentPage  │
│              │ page  │              │
└──────┬───────┘       └──────────────┘
       │
       │ comment
       ▼
┌──────────────┐
│   Reaction   │
└──────────────┘

┌──────────────┐
│    Event     │───────┐
│              │ user  │ (opcional, para cumpleaños)
└──────────────┘       ▼
                ┌──────────────┐
                │  CustomUser  │
                └──────────────┘
```

---

## 5. API REST (Wagtail)

### 5.1 Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register` | Registro con email/contraseña | No |
| POST | `/api/auth/login` | Login, retorna JWT | No |
| POST | `/api/auth/refresh` | Refrescar JWT | JWT |
| POST | `/api/auth/logout` | Invalidar tokens | JWT |
| POST | `/api/auth/password/reset` | Solicitar reset | No |
| POST | `/api/auth/password/confirm` | Confirmar nuevo password | Token |
| GET | `/api/auth/verify/{token}` | Verificar email | Token |

### 5.2 Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/users/me` | Perfil del usuario actual | JWT |
| PATCH | `/api/users/me` | Actualizar perfil | JWT |
| GET | `/api/users/` | Directorio de miembros | JWT (confirmado) |
| GET | `/api/users/pending` | Lista pendientes | JWT (admin) |
| PATCH | `/api/users/{id}/status` | Aprobar/rechazar | JWT (admin) |

### 5.3 Contenido

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/pages/` | Lista de páginas públicas | No |
| GET | `/api/pages/{slug}` | Detalle de página | Condicional |
| GET | `/api/characters/` | Lista de personajes | No |
| GET | `/api/characters/{slug}` | Detalle de personaje | No |

### 5.4 Comentarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/pages/{id}/comments` | Comentarios de página | Condicional |
| POST | `/api/pages/{id}/comments` | Crear comentario | JWT (confirmado) |
| DELETE | `/api/comments/{id}` | Eliminar comentario | JWT (mod/admin) |
| POST | `/api/comments/{id}/reactions` | Agregar reacción | JWT (confirmado) |
| DELETE | `/api/comments/{id}/reactions/{emoji}` | Quitar reacción | JWT |

### 5.5 Eventos/Calendario

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/events/` | Lista de eventos | JWT (confirmado) |
| GET | `/api/events/calendar/{year}/{month}` | Eventos del mes | JWT (confirmado) |
| POST | `/api/events/` | Crear evento | JWT (staff) |

---

## 6. Estructura del Frontend (Next.js)

### 6.1 Estructura de Carpetas

```
src/
├── app/                      # App Router (Next.js 16+)
│   ├── (public)/            # Rutas públicas
│   │   ├── page.tsx         # Home
│   │   ├── guias/           # Guías
│   │   ├── lore/            # Historia/Lore
│   │   ├── calculadoras/    # Calculadoras
│   │   └── personajes/      # Perfiles de personajes
│   │
│   ├── (auth)/              # Rutas de autenticación
│   │   ├── login/
│   │   ├── registro/
│   │   └── verificar/
│   │
│   ├── (protected)/         # Rutas protegidas (miembros)
│   │   ├── actividades/
│   │   ├── calendario/
│   │   ├── directorio/
│   │   └── perfil/
│   │
│   ├── admin/               # Panel admin (si se necesita)
│   └── layout.tsx
│
├── components/
│   ├── ui/                  # Componentes base (botones, inputs)
│   ├── layout/              # Header, Footer, Sidebar
│   ├── content/             # Renderizado de contenido CMS
│   ├── comments/            # Sistema de comentarios
│   ├── calculators/         # Calculadoras del juego
│   └── auth/                # Formularios de auth
│
├── lib/
│   ├── api/                 # Cliente API para Wagtail
│   ├── auth/                # Lógica de autenticación
│   └── utils/               # Utilidades generales
│
├── hooks/                   # Custom hooks
├── types/                   # TypeScript types
└── styles/                  # CSS/SCSS globales
```

### 6.2 Componentes de Calculadora (React)

```typescript
// components/calculators/AscensionCalculator.tsx

interface AscensionInput {
  currentLevel: number;
  targetLevel: number;
  rarity: '3star' | '4star' | '5star';
}

interface AscensionResult {
  gold: number;
  xp: number;
  stamina: number;
  crystals: {
    n: number;
    r: number;
    sr: number;
    ssr: number;
  };
  estimatedDays: number;
}

const ASCENSION_COSTS = {
  '5star': [
    { level: 10, gold: 2000, xp: 1000, crystals: { n: 0, r: 0, sr: 0, ssr: 0 } },
    { level: 20, gold: 5000, xp: 3000, crystals: { n: 10, r: 0, sr: 0, ssr: 0 } },
    // ... resto de datos
  ]
};
```

---

## 7. Configuración de Despliegue (Dokploy)

### 7.1 Arquitectura de Despliegue

Dokploy gestiona automáticamente:
- **Traefik**: Proxy reverso, SSL, routing
- **Labels**: Configuración de dominios y puertos
- **Certificados**: Let's Encrypt automático

Solo necesitamos definir los servicios de la aplicación.

### 7.2 Servicios Docker (Individuales en Dokploy)

> **Nota:** En Dokploy cada servicio se despliega individualmente, no como Docker Compose monolítico.

#### Servicio: Frontend (Next.js)

```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

**Variables de entorno en Dokploy:**
```
NEXT_PUBLIC_API_URL=https://tudominio.com/api
NEXT_PUBLIC_SITE_URL=https://tudominio.com
```

**Puerto expuesto:** 3000

---

#### Servicio: Backend (Wagtail)

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collectstatic para archivos estáticos del admin
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

**Variables de entorno en Dokploy:**
```
DATABASE_URL=postgres://user:pass@db-host:5432/lads_db
REDIS_URL=redis://redis-host:6379/0
SECRET_KEY=<clave_secreta>
ALLOWED_HOSTS=tudominio.com
CORS_ORIGINS=https://tudominio.com

# Email
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=noreply@tudominio.com
EMAIL_PASSWORD=<contraseña>

# Cloudflare R2
R2_ACCOUNT_ID=<account_id>
R2_ACCESS_KEY_ID=<access_key>
R2_SECRET_ACCESS_KEY=<secret_key>
R2_BUCKET_NAME=lads-media
R2_PUBLIC_URL=https://media.tudominio.com
```

**Puerto expuesto:** 8000

---

#### Servicio: PostgreSQL

En Dokploy, usar el servicio de base de datos integrado o crear:

```
Imagen: postgres:16-alpine
Variables:
  POSTGRES_USER=lads_user
  POSTGRES_PASSWORD=<contraseña_segura>
  POSTGRES_DB=lads_db
Puerto: 5432
Volumen: /var/lib/postgresql/data
```

---

#### Servicio: Redis

```
Imagen: redis:7-alpine
Puerto: 6379
Volumen: /data
```

### 7.3 Configuración de Rutas en Dokploy

| Servicio | Dominio | Path | Puerto |
|----------|---------|------|--------|
| Frontend | tudominio.com | `/` (excepto /api y /admin) | 3000 |
| Backend | tudominio.com | `/api/*`, `/admin/*` | 8000 |

> Dokploy permite configurar path-based routing en la UI al asignar dominios.

### 7.2 Variables de Entorno (.env)

```bash
# Dominio
DOMAIN=tudominio.com

# Base de datos
DB_USER=lads_user
DB_PASSWORD=<contraseña_segura>
DB_NAME=lads_db

# Django/Wagtail
SECRET_KEY=<clave_secreta_django>
DEBUG=False

# Email (para verificación y notificaciones)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USER=noreply@tudominio.com
EMAIL_PASSWORD=<contraseña_email>

# JWT
JWT_SECRET_KEY=<clave_secreta_jwt>
JWT_EXPIRATION_DAYS=30

# Cloudflare R2 (Almacenamiento de imágenes)
R2_ACCOUNT_ID=<cloudflare_account_id>
R2_ACCESS_KEY_ID=<r2_access_key>
R2_SECRET_ACCESS_KEY=<r2_secret_key>
R2_BUCKET_NAME=lads-media
R2_PUBLIC_URL=https://media.tudominio.com
```

### 7.3 Estructura de URLs (Dominio Único)

| Ruta | Servicio | Descripción |
|------|----------|-------------|
| `tudominio.com/` | Frontend | Aplicación principal (Next.js) |
| `tudominio.com/api/` | Backend | API REST de Wagtail |
| `tudominio.com/admin/` | Wagtail Admin | Panel de administración CMS |

**Nota:** Todo en un solo dominio, sin subdominios. Traefik enruta por path prefix.

---

## 8. Seguridad

### 8.1 Autenticación JWT

```python
# Estructura del token
{
  "sub": "user_id",
  "email": "usuario@email.com",
  "role": "member",
  "status": "approved",
  "exp": 1234567890,  # 30 días desde emisión
  "iat": 1234567890
}
```

### 8.2 Middleware de Autorización

```typescript
// middleware.ts (Next.js)
export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token');
  const path = request.nextUrl.pathname;
  
  // Rutas protegidas
  if (path.startsWith('/actividades') || 
      path.startsWith('/calendario') ||
      path.startsWith('/directorio')) {
    
    if (!token) {
      return NextResponse.redirect('/login');
    }
    
    const payload = verifyToken(token);
    if (payload.status !== 'approved') {
      return NextResponse.redirect('/pendiente');
    }
  }
  
  return NextResponse.next();
}
```

---

## 9. Plan de Verificación

### 9.1 Tests Automatizados

| Tipo | Herramienta | Cobertura |
|------|-------------|-----------|
| Backend Unit | pytest | Modelos, Servicios, APIs |
| Backend Integration | pytest + TestClient | Flujos completos de API |
| Frontend Unit | Jest + RTL | Componentes, Hooks |
| Frontend E2E | Playwright | Flujos de usuario críticos |

### 9.2 Tests Manuales

| Flujo | Pasos |
|-------|-------|
| Registro | 1. Ir a /registro 2. Llenar formulario 3. Verificar email 4. Confirmar estado "pendiente" |
| Aprobación | 1. Login como admin 2. Ir a Wagtail Admin 3. Aprobar usuario 4. Verificar acceso a exclusivo |
| Comentarios | 1. Login como miembro aprobado 2. Ir a guía 3. Comentar 4. Reaccionar con emoji |

---

## 10. Decisiones de Diseño

| ID | Pregunta | Decisión |
|----|----------|----------|
| D1 | Estructura de dominio | Dominio único: `tudominio.com/`, `/api/`, `/admin/` |
| D2 | Almacenamiento de imágenes | Cloudflare R2 con URL pública `media.tudominio.com` |
| D3 | API Framework | Por definir: Django Rest Framework o Wagtail API v2 |
