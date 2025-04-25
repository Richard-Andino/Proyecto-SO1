# utils.py
import csv

def leer_procesos_desde_archivo(nombre_archivo):
    """Lee procesos desde un archivo CSV.

    El archivo CSV debe tener encabezados: ID, Llegada, Rafaga, Prioridad (opcional).
    """
    procesos = []
    try:
        with open(nombre_archivo, 'r') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for fila in lector_csv:
                proceso = {
                    'id': fila['id'],
                    'llegada': int(fila['llegada']),
                    'rafaga': int(fila['rafaga'])
                }
                if 'prioridad' in fila:
                    proceso['prioridad'] = int(fila['prioridad'])
                procesos.append(proceso)
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None
    except ValueError:
        print("Error: Asegúrate de que los tiempos de Llegada y Ráfaga sean números enteros.")
        return None
    return procesos

def generar_color(id_proceso):
    """Genera un color único para cada proceso para el diagrama de Gantt."""
    hash_val = hash(id_proceso) & 0xFFFFFF
    return '#%06x' % hash_val

if __name__ == '__main__':
    # Ejemplo de cómo leer un archivo de procesos (crea un archivo 'procesos.csv' primero)
    # con contenido como:
    # ID,Llegada,Rafaga,Prioridad
    # P1,0,5,3
    # P2,2,3,1
    # P3,4,8,2
    procesos = leer_procesos_desde_archivo('procesos.csv')
    if procesos:
        print("Procesos leídos:", procesos)