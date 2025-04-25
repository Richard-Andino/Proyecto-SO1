from collections import deque

def fcfs(procesos):
    """Algoritmo FCFS (First Come First Served)."""
    n = len(procesos)
    tiempo_actual = 0
    cola_listos = deque()
    historial = []
    tiempos_espera = [0] * n
    tiempos_retorno = [0] * n
    tiempos_respuesta = [-1] * n  # Inicializar tiempos de respuesta
    tiempo_comienzo = [-1] * n

    procesos_ordenados = sorted(procesos, key=lambda x: x['llegada'])
    indices = {proceso['id']: i for i, proceso in enumerate(procesos)}
    i = 0
    while i < n or cola_listos:
        if cola_listos:
            proceso_actual = cola_listos.popleft()
            id_actual = proceso_actual['id']
            indice = indices[id_actual]
            inicio = tiempo_actual
            if tiempo_comienzo[indice] == -1:
                tiempo_comienzo[indice] = inicio
                tiempos_respuesta[indice] = inicio - proceso_actual['llegada']
            fin = tiempo_actual + proceso_actual['rafaga']
            historial.append({'id': id_actual, 'Inicio': inicio, 'Fin': fin})
            tiempos_espera[indice] = inicio - proceso_actual['llegada']
            tiempos_retorno[indice] = fin - proceso_actual['llegada']
            tiempo_actual = fin
        else:
            tiempo_actual = procesos_ordenados[i]['llegada']

        while i < n and procesos_ordenados[i]['llegada'] <= tiempo_actual:
            cola_listos.append(procesos_ordenados[i].copy())
            i += 1

    return historial, tiempos_espera, tiempos_retorno, tiempos_respuesta

def round_robin(procesos, quantum):
    """Algoritmo Round Robin."""
    n = len(procesos)
    tiempo_actual = 0
    cola_listos = deque()
    historial = []
    tiempos_espera = [0] * n
    tiempos_retorno = [0] * n
    tiempos_respuesta = [-1] * n  # Inicializar tiempos de respuesta
    tiempo_comienzo = [-1] * n  # Para calcular el tiempo de espera correctamente
    procesos_en_cola = {p['id']: False for p in procesos} # Para rastrear si un proceso ya entró en la cola por primera vez

    procesos_restantes = {p['id']: p['rafaga'] for p in procesos}
    procesos_ordenados = sorted(procesos, key=lambda x: x['llegada'])
    indices = {proceso['id']: i for i, proceso in enumerate(procesos)}
    i = 0

    while procesos_restantes or cola_listos:
        while i < n and procesos_ordenados[i]['llegada'] <= tiempo_actual:
            proceso_llegando = procesos_ordenados[i].copy()
            if not procesos_en_cola[proceso_llegando['id']]:
                cola_listos.append(proceso_llegando)
                procesos_en_cola[proceso_llegando['id']] = True
            i += 1

        if not cola_listos:
            if i < n:
                tiempo_actual = procesos_ordenados[i]['llegada']
            else:
                break
            continue

        proceso_actual = cola_listos.popleft()
        id_actual = proceso_actual['id']
        indice = indices[id_actual]

        if tiempo_comienzo[indice] == -1:
            tiempo_comienzo[indice] = tiempo_actual
            tiempos_respuesta[indice] = tiempo_actual - [p['llegada'] for p in procesos if p['id'] == id_actual][0]

        ejecucion = min(quantum, procesos_restantes[id_actual])
        inicio = tiempo_actual
        tiempo_actual += ejecucion
        fin = tiempo_actual
        historial.append({'id': id_actual, 'Inicio': inicio, 'Fin': fin})
        procesos_restantes[id_actual] -= ejecucion

        if procesos_restantes[id_actual] > 0:
            cola_listos.append(proceso_actual)
        else:
            tiempos_retorno[indice] = tiempo_actual - [p['llegada'] for p in procesos if p['id'] == id_actual][0]
            tiempos_espera[indice] = tiempos_retorno[indice] - [p['rafaga'] for p in procesos if p['id'] == id_actual][0]
            if id_actual in procesos_restantes:
                del procesos_restantes[id_actual]

    return historial, tiempos_espera, tiempos_retorno, tiempos_respuesta

def sjf(procesos):
    """Algoritmo SJF (Shortest Job First) - No expulsivo."""
    n = len(procesos)
    tiempo_actual = 0
    cola_listos = []
    historial = []
    tiempos_espera = [0] * n
    tiempos_retorno = [0] * n
    tiempos_respuesta = [-1] * n  # Inicializar tiempos de respuesta
    tiempo_comienzo = [-1] * n
    completados = [False] * n

    procesos_ordenados_llegada = sorted(procesos, key=lambda x: x['llegada'])
    indices = {proceso['id']: i for i, proceso in enumerate(procesos)}
    i = 0

    while not all(completados):
        while i < n and procesos_ordenados_llegada[i]['llegada'] <= tiempo_actual:
            cola_listos.append(procesos_ordenados_llegada[i])
            i += 1
        cola_listos.sort(key=lambda x: x['rafaga'])  # Selecciona el de menor ráfaga

        if not cola_listos:
            tiempo_actual += 1
            continue

        proceso_actual = cola_listos.pop(0)
        id_actual = proceso_actual['id']
        indice = indices[id_actual]
        inicio = tiempo_actual
        if tiempo_comienzo[indice] == -1:
            tiempo_comienzo[indice] = inicio
            tiempos_respuesta[indice] = inicio - proceso_actual['llegada']
        fin = tiempo_actual + proceso_actual['rafaga']
        historial.append({'id': id_actual, 'Inicio': inicio, 'Fin': fin})
        tiempos_espera[indice] = inicio - proceso_actual['llegada']
        tiempos_retorno[indice] = fin - proceso_actual['llegada']
        tiempo_actual = fin
        completados[indice] = True

    return historial, tiempos_espera, tiempos_retorno, tiempos_respuesta

def prioridades(procesos):
    """Algoritmo de Prioridades - No expulsivo (menor número = mayor prioridad)."""
    n = len(procesos)
    tiempo_actual = 0
    cola_listos = []
    historial = []
    tiempos_espera = [0] * n
    tiempos_retorno = [0] * n
    tiempos_respuesta = [-1] * n  # Inicializar tiempos de respuesta
    tiempo_comienzo = [-1] * n
    completados = [False] * n

    procesos_ordenados_llegada = sorted(procesos, key=lambda x: x['llegada'])
    indices = {proceso['id']: i for i, proceso in enumerate(procesos)}
    i = 0

    while not all(completados):
        while i < n and procesos_ordenados_llegada[i]['llegada'] <= tiempo_actual:
            cola_listos.append(procesos_ordenados_llegada[i])
            i += 1
        cola_listos.sort(key=lambda x: x.get('prioridad', float('inf'))) # Prioridad más baja primero

        if not cola_listos:
            tiempo_actual += 1
            continue

        proceso_actual = cola_listos.pop(0)
        id_actual = proceso_actual['id']
        indice = indices[id_actual]
        inicio = tiempo_actual
        if tiempo_comienzo[indice] == -1:
            tiempo_comienzo[indice] = inicio
            tiempos_respuesta[indice] = inicio - proceso_actual['llegada']
        fin = tiempo_actual + proceso_actual['rafaga']
        historial.append({'id': id_actual, 'Inicio': inicio, 'Fin': fin})
        tiempos_espera[indice] = inicio - proceso_actual['llegada']
        tiempos_retorno[indice] = fin - proceso_actual['llegada']
        tiempo_actual = fin
        completados[indice] = True

    return historial, tiempos_espera, tiempos_retorno, tiempos_respuesta

if __name__ == '__main__':
    procesos_ejemplo = [
        {'id': 'P1', 'llegada': 0, 'rafaga': 5},
        {'id': 'P2', 'llegada': 2, 'rafaga': 3},
        {'id': 'P3', 'llegada': 4, 'rafaga': 8},
        {'id': 'P4', 'llegada': 6, 'rafaga': 2}
    ]
    historial_fcfs, espera_fcfs, retorno_fcfs, respuesta_fcfs = fcfs(procesos_ejemplo.copy())
    print("FCFS:", historial_fcfs, espera_fcfs, retorno_fcfs, respuesta_fcfs)

    historial_rr, espera_rr, retorno_rr, respuesta_rr = round_robin(procesos_ejemplo.copy(), 2)
    print("Round Robin:", historial_rr, espera_rr, retorno_rr, respuesta_rr)

    historial_sjf, espera_sjf, retorno_sjf, respuesta_sjf = sjf(procesos_ejemplo.copy())
    print("SJF:", historial_sjf, espera_sjf, retorno_sjf, respuesta_sjf)

    procesos_prioridad = [
        {'id': 'P1', 'llegada': 0, 'rafaga': 5, 'prioridad': 3},
        {'id': 'P2', 'llegada': 2, 'rafaga': 3, 'prioridad': 1},
        {'id': 'P3', 'llegada': 4, 'rafaga': 8, 'prioridad': 2},
        {'id': 'P4', 'llegada': 6, 'rafaga': 2, 'prioridad': 3}
    ]
    historial_prioridad, espera_prioridad, retorno_prioridad, respuesta_prioridad = prioridades(procesos_prioridad.copy())
    print("Prioridades:", historial_prioridad, espera_prioridad, retorno_prioridad, respuesta_prioridad)