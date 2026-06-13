# Uziel OS - Roadmap de desarrollo

## FASE 0 - Bootstrap tecnico dockerizado

### Objetivo
Preparar monorepo para desarrollo profesional.

### Entregables backend

- `docker-compose.yml`
- `backend/Dockerfile`
- `backend/.dockerignore`
- `backend/entrypoint.sh`
- `backend/.env.example`
- `backend/requirements.txt`
- Settings separados: base, local, production.
- PostgreSQL conectado.
- Redis disponible.
- Celery preparado.
- `GET /api/health/`.

### Entregables frontend

- Estructura `src/app`, `src/shared`, `src/features`.
- Vue Router.
- Pinia.
- Cliente API centralizado.
- Variables CSS globales.
- Layout base.
- `frontend/.env.example`.

### Criterios de aceptacion

```bash
docker compose up --build
docker compose exec backend python manage.py check
docker compose exec backend python manage.py migrate
```

`GET /api/health/` responde `status: ok`.

`npm run dev` funciona en frontend.

---

## FASE 0.5 - Backend activo + Frontend preparado sin UI final

### Objetivo
Asegurar que backend corra completo con Docker y frontend esté estructurado técnicamente, sin implementar diseño visual final esperando a Figma.

### Tareas por Agente

**Agente Backend:**
- Configurar y levantar Docker Compose con PostgreSQL, Redis, backend.
- Crear proyecto Django y configuración básica.
- Crear endpoint `GET /api/health/`.
- Validar migraciones.

**Agente Frontend:**
- Configurar Vite + Vue 3 + TS.
- Configurar Router y Pinia (archivos base).
- Configurar cliente API apuntando a `localhost:8000/api/`.
- Consumir `GET /api/health/` desde App.vue como placeholder.

**Agente UI:**
- Crear estructura de carpetas de estilos CSS.
- Declarar variables CSS base.
- NO crear componentes definitivos.

**Agente QA:**
- Validar `docker compose up --build`.
- Validar `GET /api/health/` desde backend y frontend.
- Validar ausencia de secretos y correcta estructura de `.env.example`.

### Criterios de Aceptación FASE 0.5
- docker compose up --build levanta backend, db y redis.
- backend puede ejecutar migraciones.
- GET /api/health/ responde correctamente.
- frontend corre con npm run dev.
- frontend puede consumir /api/health/.
- no hay pantallas visuales finales implementadas.
- existen placeholders técnicos.
- existen .env.example actualizados.
- no hay secretos hardcodeados.
- README tiene comandos claros.

---

## FASE 1 - Dominio base de rutinas

- Categorias.
- RoutineTemplate.
- RoutineScheduleRule.
- CRUD de rutinas.
- Seeds iniciales.
- Tests de modelos.

---

## FASE 2 - Agenda diaria y ejecuciones

- Generar ejecuciones del dia.
- `GET /api/schedule/today/`.
- Vista Agenda.
- Estados iniciales.

---

## FASE 3 - Maquina de estados

- `start`, `pause`, `resume`, `complete`, `snooze`, `omit`.
- Validacion de transiciones.
- Transacciones atomicas.
- Tests de reglas.

---

## FASE 4 - Dashboard visual

- Progreso diario.
- Minutos por ambito.
- Rachas.
- Graficos.
- Cards minimalistas.

---

## FASE 5 - Notificaciones PWA

- Permisos.
- Device register.
- Web Push base.
- Notificacion de prueba.
- Fallback de apertura.

---

## FASE 6 - Celery y automatizacion

- Celery Worker.
- Celery Beat.
- Deteccion de rutinas proximas.
- Auto-completado de rutinas iniciadas.
- Vencimiento de rutinas no iniciadas.

---

## FASE 7 - Mobile confiable con Capacitor

- Build movil.
- Notificaciones locales.
- Acciones moviles.
- Pruebas en celular.

---

## FASE 8 - Reportes e insights

- Reporte semanal.
- Insights simples.
- Cruces: sueno vs foco, alimentacion vs energia.

---

## FASE 9 - Pulido y deploy

- Testing E2E.
- Seguridad.
- Docker produccion.
- Deploy backend.
- Deploy frontend.
