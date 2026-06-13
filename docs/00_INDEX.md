# Uziel OS - Indice de documentacion

Este directorio contiene la documentacion oficial para construir Uziel OS con agentes de IA en Antigravity.

Uziel OS es un sistema personal de alto rendimiento. Su objetivo es orquestar rutinas diarias de higiene, ejercicio, foco/trabajo, alimentacion y sueno mediante agenda, notificaciones accionables, motor de estados y dashboard visual.

## Estado actual del proyecto

El monorepo esta en fase inicial. No se debe construir funcionalidad compleja hasta completar la base tecnica.

## Fase actual obligatoria: FASE 0 - Bootstrap tecnico dockerizado

Antes de implementar rutinas, dashboard, autenticacion compleja o notificaciones reales, el equipo de agentes debe dejar lista la base tecnica del monorepo.

### Objetivo de FASE 0

Levantar correctamente:

- Backend Django REST Framework en Docker.
- PostgreSQL en contenedor.
- Redis en contenedor.
- Celery Worker preparado para tareas asincronas.
- Celery Beat preparado para tareas programadas.
- Frontend Vue 3 + TypeScript + Vite con estructura limpia.
- Variables globales de diseno con CSS custom properties.
- Archivos `.env.example` para backend y frontend.
- Endpoint `GET /api/health/` funcionando.
- README con comandos para desarrollo.

## Documentos incluidos

| Archivo | Proposito |
|---|---|
| `01_PRODUCT_REQUIREMENTS.md` | Vision, alcance, requerimientos funcionales y no funcionales. |
| `02_AI_AGENT_RULES.md` | Reglas estrictas para agentes de IA. |
| `03_MONOREPO_STRUCTURE.md` | Estructura esperada del repositorio. |
| `04_DESIGN_SYSTEM.md` | Variables CSS, colores, tipografia y UI minimalista. |
| `05_FRONTEND_ARCHITECTURE.md` | Arquitectura limpia del frontend Vue. |
| `06_BACKEND_ARCHITECTURE.md` | Arquitectura limpia del backend DRF dockerizado. |
| `07_DATABASE_MODEL.md` | Modelo de datos inicial. |
| `08_API_CONTRACT.md` | Contrato REST inicial. |
| `09_NOTIFICATION_ENGINE.md` | Motor de notificaciones y estados. |
| `10_USE_CASES.md` | Casos de uso funcionales del MVP. |
| `11_ENVIRONMENT_VARIABLES.md` | Variables de entorno requeridas. |
| `12_DEVELOPMENT_ROADMAP.md` | Fases de implementacion. |
| `13_TESTING_AND_QUALITY.md` | Calidad, pruebas y criterios de aceptacion. |
| `14_AGENT_PROMPTS.md` | Prompts listos para orquestar agentes en Antigravity. |

## Checkpoint para cerrar FASE 0

La FASE 0 solo se considera completa si:

```bash
docker compose up --build
```

levanta correctamente al menos:

- `backend`
- `db`
- `redis`

Y despues funcionan:

```bash
docker compose exec backend python manage.py check
docker compose exec backend python manage.py migrate
```

Ademas:

```txt
GET http://localhost:8000/api/health/
```

debe responder:

```json
{
  "status": "ok",
  "service": "uziel-os-api"
}
```

El frontend debe correr con:

```bash
cd frontend
npm install
npm run dev
```

Y debe poder leer la URL del backend desde:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

## Regla principal

No se debe improvisar. Cada agente debe leer estos documentos antes de modificar codigo.
