# Uziel OS - Estructura del monorepo

## 1. Estructura esperada

```txt
ROUTINEGOPROJECT/
├── backend/
│   ├── apps/
│   │   ├── accounts/
│   │   ├── analytics/
│   │   ├── common/
│   │   ├── executions/
│   │   ├── notifications/
│   │   ├── routines/
│   │   ├── schedule/
│   │   ├── focus/
│   │   ├── nutrition/
│   │   ├── sleep/
│   │   ├── exercise/
│   │   └── hygiene/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── entrypoint.sh
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layouts/
│   │   │   ├── providers/
│   │   │   └── router/
│   │   ├── shared/
│   │   │   ├── api/
│   │   │   ├── components/
│   │   │   ├── composables/
│   │   │   ├── styles/
│   │   │   ├── types/
│   │   │   └── utils/
│   │   ├── features/
│   │   │   ├── analytics/
│   │   │   ├── dashboard/
│   │   │   ├── exercise/
│   │   │   ├── focus/
│   │   │   ├── hygiene/
│   │   │   ├── notifications/
│   │   │   ├── nutrition/
│   │   │   ├── routines/
│   │   │   ├── schedule/
│   │   │   └── sleep/
│   │   ├── App.vue
│   │   └── main.ts
│   ├── .env.example
│   ├── package.json
│   └── vite.config.ts
├── docs/
├── screenshots/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── amplify.yml
└── README.md
```

## 2. Responsabilidades por carpeta

### `/backend`

Contiene API, modelos, servicios de dominio, tareas Celery y configuracion Django.

### `/frontend`

Contiene app Vue 3, UI, dashboard, rutas, estado Pinia, cliente API y PWA.

### `/docs`

Fuente de verdad para agentes. Todo agente debe leerla antes de trabajar.

### `/screenshots`

Referencia visual, mockups y capturas del producto.

### `docker-compose.yml`

Orquesta backend, PostgreSQL, Redis y servicios Celery.

## 3. Convenciones

- Carpetas en `kebab-case` o nombres simples en minusculas.
- Apps Django en singular/plural consistente segun dominio.
- Componentes Vue en `PascalCase.vue`.
- Composables Vue con prefijo `use`.
- Tipos TypeScript en `*.types.ts`.
- Servicios API en `*.api.ts`.

## 4. Archivos que no deben versionarse

- `.env`
- `venv/`
- `node_modules/`
- archivos locales de base de datos
- caches
- logs
- builds
