# Uziel OS - Product Requirements

## 1. Vision del producto

Uziel OS sera un sistema personal de alto rendimiento para gestionar rutinas diarias mediante agenda, notificaciones, estados automaticos y dashboard visual.

El objetivo no es registrar todo, sino ejecutar las acciones correctas en el momento correcto con la menor friccion posible.

## 2. Problema que resuelve

El usuario necesita organizar su dia con recordatorios accionables para:

- Higiene personal.
- Ejercicio.
- Trabajo profundo/foco.
- Alimentacion.
- Sueno.

La app debe notificar antes de cada actividad, permitir iniciar desde la notificacion o desde la app, controlar el temporizador y actualizar graficos de progreso.

## 3. Alcance del MVP

El MVP cubre cinco ambitos:

| Ambito | Ejemplos de rutinas | Metricas motivadoras |
|---|---|---|
| Higiene | Lavarse rostro, masaje facial, yoga facial, cuidado personal | % completado, racha, puntualidad |
| Ejercicio | Yoga corporal, fuerza, cardio, movilidad | minutos activos, sesiones, consistencia |
| Foco/Trabajo | Typing, deep work, estudio, programacion | horas de foco, sesiones, distracciones |
| Alimentacion | Desayuno, comida, cena, agua, preparacion | comidas cumplidas, agua, consistencia |
| Sueno | Preparacion para dormir, hora objetivo, despertar | horas dormidas, calidad, cumplimiento |

## 4. Flujo principal

1. El usuario crea una rutina con categoria, hora, duracion, dias y aviso previo.
2. El sistema genera una ejecucion para el dia correspondiente.
3. Un minuto antes, el sistema envia una notificacion.
4. La notificacion ofrece acciones: `Iniciar`, `Posponer`, `Omitir`, cuando la plataforma lo permita.
5. Si el usuario inicia, la ejecucion pasa a `IN_PROGRESS`.
6. Al terminar la duracion configurada, el sistema marca `COMPLETED` automaticamente.
7. Si el usuario no inicia, la rutina no se auto-completa; queda vencida, omitida o pendiente segun regla.
8. El dashboard actualiza progreso, rachas y graficos.

## 5. Requerimientos funcionales

| ID | Modulo | Requerimiento | Prioridad |
|---|---|---|---|
| RF-01 | Auth | El usuario podra iniciar sesion y gestionar su cuenta | Alta |
| RF-02 | Categorias | Existiran categorias base: higiene, ejercicio, foco, alimentacion, sueno | Alta |
| RF-03 | Rutinas | Crear rutinas con nombre, instrucciones, hora, duracion, dias, aviso previo y prioridad | Alta |
| RF-04 | Agenda | Mostrar rutinas del dia ordenadas por hora y estado | Alta |
| RF-05 | Ejecuciones | Generar instancias diarias de cada rutina programada | Alta |
| RF-06 | Notificaciones | Enviar notificacion previa segun `reminder_minutes` | Alta |
| RF-07 | Acciones | Iniciar, posponer u omitir desde notificacion cuando sea posible | Alta |
| RF-08 | Fallback | Si no hay acciones en notificacion, abrir pantalla de ejecucion | Alta |
| RF-09 | Temporizador | Mostrar tiempo restante y progreso de la rutina iniciada | Alta |
| RF-10 | Auto-completado | Completar automaticamente solo rutinas iniciadas | Alta |
| RF-11 | Dashboard | Mostrar progreso diario, semanal y mensual con graficos | Alta |
| RF-12 | Rachas | Calcular dias consecutivos de cumplimiento | Media |
| RF-13 | Sueno | Registrar hora de dormir, despertar, horas y calidad | Media |
| RF-14 | Alimentacion | Registrar comidas programadas, completadas y agua | Media |
| RF-15 | Foco | Registrar sesiones de foco, objetivos y distracciones | Media |
| RF-16 | Reportes | Mostrar resumen semanal e insights simples | Media |
| RF-17 | Configuracion | Gestionar permisos, dispositivos y pruebas de notificacion | Alta |
| RF-18 | Exportacion | Exportar datos basicos a CSV/JSON | Baja |

## 6. Requerimientos no funcionales

| ID | Atributo | Requerimiento |
|---|---|---|
| RNF-01 | Usabilidad | Iniciar una rutina debe tomar menos de 3 clics desde dashboard |
| RNF-02 | Rendimiento | Dashboard inicial debe cargar rapido con datos cacheados |
| RNF-03 | Portabilidad | UI responsive para PC, tablet y celular |
| RNF-04 | Seguridad | API protegida con autenticacion, permisos por usuario y validaciones |
| RNF-05 | Privacidad | Notificaciones sin informacion sensible por defecto |
| RNF-06 | Mantenibilidad | Arquitectura por dominios, servicios y contratos claros |
| RNF-07 | Observabilidad | Logs para errores, notificaciones y transiciones de estado |
| RNF-08 | Configuracion | Secretos y credenciales solo mediante variables de entorno |

## 7. Criterios de exito del MVP

- Crear una rutina en menos de 1 minuto.
- Recibir notificacion previa.
- Iniciar rutina desde notificacion o desde app.
- Completar automaticamente solo cuando fue iniciada.
- Ver progreso por categoria en graficos.
- Usar la app en escritorio y celular.
- Mantener codigo limpio y modular.
