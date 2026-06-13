# Uziel OS - Testing and Quality

## 1. Principios

Cada fase debe cerrar con pruebas claras. No se avanza si la base no corre.

## 2. Checklist FASE 0

### Docker

- [ ] `docker compose build` funciona.
- [ ] `docker compose up` levanta servicios.
- [ ] `backend` inicia sin errores.
- [ ] `db` PostgreSQL esta disponible.
- [ ] `redis` esta disponible.
- [ ] El volumen de PostgreSQL persiste datos.
- [ ] No se usa SQLite como base principal.

### Backend

- [ ] `docker compose exec backend python manage.py check` funciona.
- [ ] `docker compose exec backend python manage.py migrate` funciona.
- [ ] `GET /api/health/` responde correctamente.
- [ ] CORS permite frontend local.
- [ ] `.env.example` existe y no contiene secretos reales.

### Frontend

- [ ] `npm install` funciona.
- [ ] `npm run dev` funciona.
- [ ] `npm run build` funciona.
- [ ] Variables CSS globales existen.
- [ ] No hay colores hardcodeados innecesarios.
- [ ] Cliente API lee `VITE_API_BASE_URL`.

## 3. Pruebas backend futuras

- Unit tests de maquina de estados.
- Tests de servicios de agenda.
- Tests de permisos por usuario.
- Tests de Celery idempotente.
- API tests para start/snooze/omit/complete.

## 4. Pruebas frontend futuras

- Componentes base.
- Stores Pinia.
- Composables.
- Estados loading/error/empty/success.
- Responsive desktop/mobile.

## 5. E2E futuro

Flujo principal:

1. Crear rutina.
2. Generar ejecucion.
3. Recibir notificacion o simularla.
4. Iniciar rutina.
5. Completar automaticamente.
6. Ver dashboard actualizado.

## 6. Criterios de calidad

- Codigo claro.
- Nombres descriptivos.
- Servicios de dominio.
- Sin duplicacion innecesaria.
- Sin secretos hardcodeados.
- Documentacion actualizada.
- Comandos reproducibles.
