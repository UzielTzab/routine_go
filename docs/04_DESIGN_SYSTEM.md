# Uziel OS - Design System

## 1. Principios de UI

La interfaz debe ser:

- Minimalista.
- Limpia.
- Rapida.
- Motivadora.
- Mobile-first.
- Basada en tarjetas, graficos y microinteracciones.

**NOTA IMPORTANTE:** Los tokens definitivos de diseño, colores exactos y proporciones dependen del diseño final de Figma. Hasta su aprobación, usar los valores base por defecto como placeholders.

## 2. Variables globales

Todos los estilos globales deben vivir en:

```txt
frontend/src/shared/styles/
├── variables.css
├── reset.css
├── typography.css
├── layout.css
├── utilities.css
└── index.css
```

`index.css` debe importar el resto.

## 3. Variables CSS obligatorias

```css
:root {
  --font-sans: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

  --color-primary: #635bff;
  --color-primary-soft: #eef0ff;
  --color-primary-strong: #4338ca;

  --color-hygiene: #3b82f6;
  --color-hygiene-soft: #dbeafe;
  --color-exercise: #22c55e;
  --color-exercise-soft: #dcfce7;
  --color-focus: #8b5cf6;
  --color-focus-soft: #ede9fe;
  --color-nutrition: #f97316;
  --color-nutrition-soft: #ffedd5;
  --color-sleep: #6366f1;
  --color-sleep-soft: #e0e7ff;

  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-danger: #ef4444;
  --color-info: #0ea5e9;

  --background-app: #f8fafc;
  --background-elevated: #ffffff;
  --surface-card: #ffffff;
  --surface-muted: #f1f5f9;
  --surface-soft: #f8fafc;

  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --text-inverse: #ffffff;

  --border-soft: #e2e8f0;
  --border-strong: #cbd5e1;

  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.25rem;
  --radius-2xl: 1.5rem;
  --radius-full: 999px;

  --shadow-soft: 0 8px 20px rgba(15, 23, 42, 0.04);
  --shadow-card: 0 12px 30px rgba(15, 23, 42, 0.06);
  --shadow-floating: 0 20px 45px rgba(15, 23, 42, 0.10);

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;

  --sidebar-width: 17rem;
  --bottom-nav-height: 4.5rem;
  --topbar-height: 4.5rem;

  --z-dropdown: 20;
  --z-sticky: 30;
  --z-modal: 50;
  --z-toast: 70;
}
```

## 4. Uso correcto

Correcto:

```css
.card {
  background: var(--surface-card);
  color: var(--text-primary);
  border: 1px solid var(--border-soft);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card);
}
```

Incorrecto:

```css
.card {
  background: white;
  color: #111827;
  border-radius: 20px;
}
```

## 5. Componentes base esperados

- `BaseButton`
- `BaseCard`
- `BaseInput`
- `BaseSelect`
- `BaseModal`
- `BaseBadge`
- `ProgressRing`
- `ProgressBar`
- `MetricCard`
- `EmptyState`
- `LoadingState`
- `ErrorState`

## 6. Layouts

### Desktop

- Sidebar izquierda.
- Topbar superior.
- Grid de tarjetas.
- Dashboard amplio.

### Mobile

- Header compacto.
- Cards verticales.
- Bottom navigation.
- Acciones principales visibles.

## 7. Colores por categoria

| Categoria | Variable | Uso |
|---|---|---|
| Higiene | `--color-hygiene` | cuidado personal |
| Ejercicio | `--color-exercise` | actividad fisica |
| Foco | `--color-focus` | trabajo profundo |
| Alimentacion | `--color-nutrition` | comidas/agua |
| Sueno | `--color-sleep` | descanso |

## 8. Regla de UX

El usuario debe entender en menos de 5 segundos:

- Que toca hacer ahora.
- Que sigue despues.
- Que progreso lleva.
- Donde esta atrasado.
