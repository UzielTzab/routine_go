# Uziel OS - Casos de uso

## CU-01 - Crear rutina programada

**Actor:** Usuario principal  
**Prioridad:** Alta

### Objetivo
Crear una rutina recurrente o puntual con horario, duracion, categoria y notificacion previa.

### Flujo principal

1. El usuario abre Rutinas.
2. Presiona Nueva rutina.
3. Elige categoria.
4. Captura nombre, instrucciones, hora, duracion, dias y aviso previo.
5. Guarda.
6. El sistema crea la rutina y genera futuras ejecuciones.

### Excepciones

- Si faltan datos, mostrar validacion clara.
- Si no hay permisos de notificacion, mostrar guia.

## CU-02 - Recibir notificacion previa

**Actor:** Sistema de notificaciones  
**Prioridad:** Alta

### Flujo principal

1. Un minuto antes de la rutina, el motor detecta ejecucion proxima.
2. El sistema envia notificacion.
3. La notificacion muestra nombre, categoria, duracion y acciones.
4. La ejecucion queda en `NOTIFIED`.

### Excepciones

- Si no hay botones, abrir pantalla de ejecucion.
- Si esta offline, usar fallback local cuando exista Capacitor.

## CU-03 - Iniciar rutina desde notificacion

**Actor:** Usuario principal  
**Prioridad:** Alta

### Flujo principal

1. El usuario toca `Iniciar`.
2. Service Worker o app nativa captura la accion.
3. Se llama `POST /api/executions/{id}/start/`.
4. Backend valida permisos y transicion.
5. Estado cambia a `IN_PROGRESS`.
6. Temporizador inicia.

## CU-04 - Auto-completar rutina iniciada

**Actor:** Motor de rutinas  
**Prioridad:** Alta

### Flujo principal

1. El motor calcula `actual_start + duration_minutes`.
2. Al llegar la hora final, valida que siga `IN_PROGRESS`.
3. Cambia a `COMPLETED`.
4. Guarda `actual_end`.
5. Actualiza analytics.

### Regla critica

Si la rutina nunca fue iniciada, no se auto-completa.

## CU-05 - Posponer rutina

1. Usuario toca `Posponer`.
2. Selecciona 5, 10 o 15 minutos.
3. El sistema cambia a `SNOOZED`.
4. Se reprograma notificacion.

## CU-06 - Omitir rutina

1. Usuario toca `Omitir`.
2. Opcionalmente registra motivo.
3. El sistema cambia a `OMITTED`.
4. Analytics lo registra como dato util, pero no suma completado.

## CU-07 - Consultar dashboard diario

1. Usuario abre Dashboard.
2. Ve tarjetas por categoria.
3. Revisa rutina actual y siguiente.
4. Ve graficos de progreso.
5. Entra a detalle si desea.

## CU-08 - Registrar sueno

1. Sistema notifica preparacion para dormir.
2. Usuario inicia o completa rutina nocturna.
3. Al despertar, registra hora y calidad.
4. Dashboard cruza sueno con foco/energia.

## CU-09 - Registrar alimentacion

1. Sistema notifica desayuno/comida/cena.
2. Usuario inicia o marca como completado.
3. Puede agregar nota rapida.
4. Dashboard actualiza consistencia.

## CU-10 - Ver reporte semanal

1. Usuario abre Reportes.
2. Selecciona semana.
3. Ve cumplimiento por categoria, rachas y minutos.
4. Lee insights.
5. Ajusta siguiente semana.

## CU-11 - Configurar permisos y dispositivos

1. Usuario abre Configuracion > Notificaciones.
2. Solicita permisos.
3. Envia notificacion de prueba.
4. Registra dispositivo/token.
5. Muestra estado del dispositivo.

## CU-12 - Replanificar dia

1. Usuario abre Plan del dia.
2. Presiona Replanificar.
3. El sistema mueve pendientes segun prioridad.
4. Actualiza agenda y notificaciones.
