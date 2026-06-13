# Uziel OS - Reglas para agentes de IA

Este documento define como deben trabajar los agentes de IA dentro del monorepo. Es obligatorio leerlo antes de modificar codigo.

## 1. Regla principal

No construir todo de una vez. Cada agente trabaja por fase, dominio y archivos permitidos.

## 2. Roles sugeridos

| Rol | Responsabilidad |
|---|---|
| Orquestador / Tech Lead | Divide fases, revisa arquitectura, protege reglas y documenta decisiones |
| Backend Engineer | Implementa backend DRF, Docker, PostgreSQL, Redis, servicios y tests |
| Frontend Engineer | Implementa Vue, Router, Pinia, cliente API y features |
| UI / Design System | Variables CSS, componentes base, layout y consistencia visual |
| QA / Testing | Pruebas, checklist, comandos, calidad y documentacion de validacion |

## 3. Reglas de cambios

Antes de modificar codigo, cada agente debe indicar:

1. Objetivo de la tarea.
2. Archivos que tocara.
3. Riesgos.
4. Como se probara.

Despues de modificar codigo, cada agente debe entregar:

1. Resumen de cambios.
2. Archivos modificados.
3. Comandos ejecutados.
4. Resultado de pruebas.
5. Pendientes.

## 4. Regla de backend dockerizado

El backend debe asumirse como dockerizado desde FASE 0.

Prohibido:

- Usar SQLite como base principal de desarrollo.
- Depender del `venv` local como forma oficial de ejecucion.
- Hardcodear credenciales.
- Subir `.env` real a GitHub.

Obligatorio:

- `docker-compose.yml` en la raiz.
- Servicio `backend` con Django REST Framework.
- Servicio `db` con PostgreSQL.
- Servicio `redis` con Redis.
- Preparacion para `celery_worker` y `celery_beat`.
- `.env.example` documentado.

## 5. Regla de backend como fuente de verdad

El frontend no debe decidir reglas criticas del negocio.

Deben vivir en backend:

- Transiciones de estado.
- Auto-completado.
- Permisos de usuario.
- Validacion de ejecuciones.
- Generacion de agenda.
- Calculo de metricas oficiales.

## 6. Regla de servicios de dominio

No meter reglas importantes en ViewSets o views.

Usar servicios como:

- `RoutinePlannerService`
- `ExecutionStateMachine`
- `NotificationSchedulerService`
- `AutoCompletionService`
- `AnalyticsService`

## 7. Regla frontend

Prohibido:

- `fetch` directo dentro de componentes visuales.
- Colores hardcodeados.
- Componentes gigantes con logica mezclada.
- Un store global enorme.

Obligatorio:

- `shared/api` para cliente HTTP.
- `features/*` para dominios.
- Pinia por dominio.
- Componentes reutilizables.
- Estados `loading`, `empty`, `error`, `success`.
- Variables CSS globales.

## 8. Regla de UI

Toda decision visual reutilizable debe ir en CSS variables:

- colores,
- tipografia,
- sombras,
- radios,
- espaciado,
- z-index,
- colores por categoria.

No usar valores sueltos si ya existe una variable.

## 9. Regla de notificaciones

Las notificaciones accionables dependen del navegador/sistema operativo. Por eso:

- Si hay botones, se usan `Iniciar`, `Posponer`, `Omitir`.
- Si no hay botones, tocar la notificacion abre la pantalla de ejecucion.
- Una rutina no se auto-completa si nunca fue iniciada.
- Capacitor se reserva para mejorar confiabilidad movil.

## 10. Regla de seguridad

- Ningun secreto en codigo.
- Usar `.env` local y `.env.example` versionado.
- Validar ownership por usuario en cada endpoint.
- No confiar en acciones del frontend.
- Logs utiles, sin exponer secretos.

## 11. Archivos fuera de alcance

Un agente no debe modificar dominios que no le pertenecen salvo que el Orquestador lo autorice.
