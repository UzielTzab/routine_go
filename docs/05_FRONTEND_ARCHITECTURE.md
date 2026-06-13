# Uziel OS - Frontend Architecture

## 1. Stack frontend

- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- CSS variables globales
- Chart.js, ECharts o ApexCharts para graficos
- vite-plugin-pwa para instalacion PWA
- Capacitor en fase movil posterior

**NOTA IMPORTANTE FASE 0.5:** No se debe implementar UI final ni componentes visuales definitivos hasta que el diseño final de Figma sea aprobado. Solo se permiten placeholders técnicos.

## 2. Estructura de carpetas

```txt
frontend/src/
├── app/
│   ├── router/
│   ├── layouts/
│   └── providers/
├── shared/
│   ├── api/
│   ├── components/
│   ├── composables/
│   ├── styles/
│   ├── types/
│   └── utils/
├── features/
│   ├── dashboard/
│   ├── routines/
│   ├── schedule/
│   ├── focus/
│   ├── nutrition/
│   ├── sleep/
│   ├── exercise/
│   ├── hygiene/
│   ├── analytics/
│   └── notifications/
├── App.vue
└── main.ts
```

## 3. Responsabilidades

| Carpeta | Responsabilidad |
|---|---|
| `app/router` | Rutas y guards |
| `app/layouts` | Layout desktop, mobile y auth |
| `app/providers` | Registro de plugins |
| `shared/api` | Cliente HTTP centralizado |
| `shared/components` | Componentes visuales reutilizables |
| `shared/composables` | Logica reutilizable |
| `shared/styles` | Variables y estilos globales |
| `shared/types` | Tipos globales |
| `features/*` | Funcionalidad por dominio |

## 4. Regla de API

No hacer llamadas HTTP directas desde componentes visuales.

Correcto:

```txt
Component -> composable/store -> api service -> backend
```

Incorrecto:

```txt
Component -> fetch('/api/...')
```

## 5. Cliente API esperado

Crear en:

```txt
frontend/src/shared/api/httpClient.ts
```

Debe:

- Leer `VITE_API_BASE_URL`.
- Manejar errores comunes.
- Prepararse para tokens de autenticacion.
- Devolver datos tipados.

## 6. Stores Pinia sugeridos

- `useAuthStore`
- `useRoutineStore`
- `useScheduleStore`
- `useExecutionStore`
- `useAnalyticsStore`
- `useNotificationStore`

## 7. Rutas iniciales

| Ruta | Vista |
|---|---|
| `/` | Dashboard |
| `/routines` | Gestion de rutinas |
| `/schedule` | Agenda diaria |
| `/focus` | Sesion de foco |
| `/analytics` | Graficos y reportes |
| `/notifications` | Permisos y dispositivos |
| `/settings` | Configuracion |

## 8. Estados visuales obligatorios

Toda pantalla que consuma datos debe contemplar:

- Loading.
- Empty.
- Error.
- Success.

## 9. PWA

La PWA se implementara despues de la base tecnica. Debe permitir:

- Instalacion.
- Cache basico.
- Service Worker.
- Preparacion para notificaciones web.

## 10. Mobile

La UI debe ser mobile-first. Capacitor se implementara posteriormente para notificaciones locales mas confiables.
