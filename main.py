import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk  # Para el widget Table
import algoritmos
import utils

class Proceso:
    def __init__(self, id, llegada, rafaga, prioridad=None):
        self.id = id
        self.llegada = int(llegada)
        self.rafaga = int(rafaga)
        self.prioridad = int(prioridad) if prioridad is not None else None

class SimuladorPlanificacion:
    def __init__(self, root):
        print("Inicializando SimuladorPlanificacion...")
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")
        print("Título de la ventana configurado.")

        self.procesos = []
        self.quantum = tk.IntVar(value=2) # Valor por defecto del quantum

        # --- Frame para la entrada de procesos ---
        self.frame_entrada = ttk.LabelFrame(root, text="Entrada de Procesos")
        self.frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.frame_entrada, text="Id:").grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = ttk.Entry(self.frame_entrada)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame_entrada, text="Llegada:").grid(row=1, column=0, padx=5, pady=5)
        self.llegada_entry = ttk.Entry(self.frame_entrada)
        self.llegada_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame_entrada, text="Ráfaga:").grid(row=2, column=0, padx=5, pady=5)
        self.rafaga_entry = ttk.Entry(self.frame_entrada)
        self.rafaga_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame_entrada, text="Prioridad (opcional):").grid(row=3, column=0, padx=5, pady=5)
        self.prioridad_entry = ttk.Entry(self.frame_entrada)
        self.prioridad_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.frame_entrada, text="Agregar Proceso", command=self.agregar_proceso).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame_entrada, text="Cargar desde Archivo", command=self.cargar_desde_archivo).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(self.frame_entrada, text="Limpiar", command=self.limpiar_tabla, width=10).grid(row=6, column=0, columnspan=2, pady=2)
        
        # --- Frame para la tabla de procesos ---
        self.frame_tabla = ttk.LabelFrame(root, text="Lista de Procesos")
        self.frame_tabla.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.tabla_procesos = ttk.Treeview(self.frame_tabla, columns=("ID", "Llegada", "Rafaga", "Prioridad"))
        self.tabla_procesos.heading("#1", text="ID")
        self.tabla_procesos.heading("#2", text="Llegada")
        self.tabla_procesos.heading("#3", text="Ráfaga")
        self.tabla_procesos.heading("#4", text="Prioridad")
        self.tabla_procesos.pack(fill="x")

        # --- Frame para la selección de algoritmo y quantum ---
        self.frame_algoritmo = ttk.LabelFrame(root, text="Selección de Algoritmo")
        self.frame_algoritmo.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(self.frame_algoritmo, text="Algoritmo:").grid(row=0, column=0, padx=5, pady=5)
        self.algoritmo_seleccionado = tk.StringVar(value="FCFS")
        algoritmos = ["FCFS", "Round Robin", "SJF", "Prioridades"]
        self.algoritmo_combo = ttk.Combobox(self.frame_algoritmo, textvariable=self.algoritmo_seleccionado, values=algoritmos)
        self.algoritmo_combo.grid(row=0, column=1, padx=5, pady=5)

        self.quantum_label = ttk.Label(self.frame_algoritmo, text="Quantum:")
        self.quantum_entry = ttk.Entry(self.frame_algoritmo, textvariable=self.quantum)

        self.algoritmo_seleccionado.trace_add("write", self.actualizar_interfaz_quantum)
        print("Constructor de SimuladorPlanificacion completado.")

    def actualizar_interfaz_quantum(self, *args):
        algoritmo = self.algoritmo_seleccionado.get()
        if algoritmo == "Round Robin":
            self.quantum_label.grid(row=1, column=0, padx=5, pady=5)
            self.quantum_entry.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.quantum_label.grid_forget()
            self.quantum_entry.grid_forget()

    def limpiar_tabla(self):
        """Limpia todos los procesos de la tabla y de la lista interna"""
        for item in self.tabla_procesos.get_children():
            self.tabla_procesos.delete(item)
        self.procesos = []
        print("Tabla de procesos limpiada")
    
    def agregar_proceso(self):
        id_proceso = self.id_entry.get()
        llegada = self.llegada_entry.get()
        rafaga = self.rafaga_entry.get()
        prioridad = self.prioridad_entry.get()

        if not all([id_proceso, llegada, rafaga]):
            messagebox.showerror("Error", "Por favor, complete ID, Llegada y Ráfaga.")
            return

        try:
            llegada = int(llegada)
            rafaga = int(rafaga)
            prioridad = int(prioridad) if prioridad else None
            proceso = Proceso(id_proceso, llegada, rafaga, prioridad)
            self.procesos.append(proceso.__dict__) # Guardar como diccionario
            self.actualizar_tabla_procesos()
            self.limpiar_campos_entrada()
        except ValueError:
            messagebox.showerror("Error", "Los tiempos de Llegada y Ráfaga deben ser números enteros.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def limpiar_campos_entrada(self):
        self.id_entry.delete(0, tk.END)
        self.llegada_entry.delete(0, tk.END)
        self.rafaga_entry.delete(0, tk.END)
        self.prioridad_entry.delete(0, tk.END)

    def cargar_desde_archivo(self):
        nombre_archivo = filedialog.askopenfilename(
            defaultextension=".csv",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        if nombre_archivo:
            procesos_cargados = utils.leer_procesos_desde_archivo(nombre_archivo)
            if procesos_cargados:
                self.procesos.extend(procesos_cargados)
                self.actualizar_tabla_procesos()

    def actualizar_tabla_procesos(self):
        for item in self.tabla_procesos.get_children():
            self.tabla_procesos.delete(item)
        for proceso in self.procesos:
            try:
                self.tabla_procesos.insert("", tk.END, values=(proceso['id'], proceso['llegada'], proceso['rafaga'], proceso.get('prioridad', 'N/A')))
            except KeyError as e:
                messagebox.showerror("Error al mostrar proceso", f"Falta la clave: {e}")
                print(f"Error al insertar en tabla: Falta la clave {e} en el proceso: {proceso}")
                continue

    def simular(self):
        if not self.procesos:
            messagebox.showinfo("Información", "Por favor, ingrese o cargue procesos para simular.")
            return

        algoritmo = self.algoritmo_seleccionado.get()
        quantum_value = self.quantum.get()

        if algoritmo == "Round Robin" and quantum_value <= 0:
            messagebox.showerror("Error", "El quantum debe ser mayor que cero para Round Robin.")
            return

        procesos_para_simular = [dict(p) for p in self.procesos] # Crear una copia
        rafaga_total = sum(p['rafaga'] for p in procesos_para_simular)

        if algoritmo == "FCFS":
            historial, espera, retorno, respuesta = algoritmos.fcfs(procesos_para_simular)
            tiempo_finalizacion = max(evento['Fin'] for evento in historial) if historial else 0
            uso_cpu = (rafaga_total / tiempo_finalizacion) * 100 if tiempo_finalizacion > 0 else 0
            self.mostrar_resultados(historial, espera, retorno, respuesta, uso_cpu, "FCFS")
        elif algoritmo == "Round Robin":
            historial, espera, retorno, respuesta = algoritmos.round_robin(procesos_para_simular, quantum_value)
            tiempo_finalizacion = max(evento['Fin'] for evento in historial) if historial else 0
            uso_cpu = (rafaga_total / tiempo_finalizacion) * 100 if tiempo_finalizacion > 0 else 0
            self.mostrar_resultados(historial, espera, retorno, respuesta, uso_cpu, f"Round Robin (Quantum={quantum_value})")
        elif algoritmo == "SJF":
            historial, espera, retorno, respuesta = algoritmos.sjf(procesos_para_simular)
            tiempo_finalizacion = max(evento['Fin'] for evento in historial) if historial else 0
            uso_cpu = (rafaga_total / tiempo_finalizacion) * 100 if tiempo_finalizacion > 0 else 0
            self.mostrar_resultados(historial, espera, retorno, respuesta, uso_cpu, "SJF")
        elif algoritmo == "Prioridades":
            # Asegurarse de que todos los procesos tengan prioridad (corregido la clave)
            if not all('prioridad' in p for p in procesos_para_simular):
                messagebox.showerror("Error", "Todos los procesos deben tener una prioridad definida para el algoritmo de Prioridades.")
                return
            historial, espera, retorno, respuesta = algoritmos.prioridades(procesos_para_simular)
            tiempo_finalizacion = max(evento['Fin'] for evento in historial) if historial else 0
            uso_cpu = (rafaga_total / tiempo_finalizacion) * 100 if tiempo_finalizacion > 0 else 0
            self.mostrar_resultados(historial, espera, retorno, respuesta, uso_cpu, "Prioridades")

    def mostrar_resultados(self, historial, espera, retorno, respuesta, uso_cpu, nombre_algoritmo):
        ventana_resultados = tk.Toplevel(self.root)
        ventana_resultados.title(f"Resultados de {nombre_algoritmo}")

        # Diagrama de Gantt
        canvas_alto = 200
        min_tiempo = 0
        max_tiempo = 0
        if historial:
            min_tiempo = min(item['Inicio'] for item in historial)
            max_tiempo = max(item['Fin'] for item in historial)

        # Calcular un ancho de lienzo basado en el tiempo total de simulación
        canvas_ancho = max(900, (max_tiempo - min_tiempo) * 30 + 50) # Aumenté el valor mínimo a 900
        canvas = tk.Canvas(ventana_resultados, width=canvas_ancho, height=canvas_alto, bg="white")
        canvas.pack(pady=10, fill="x", expand=True) # Permitir que se expanda horizontalmente

        if max_tiempo > min_tiempo:
            escala_x = canvas_ancho / (max_tiempo - min_tiempo)
        else:
            escala_x = 20 # Valor por defecto

        y_pos = 50
        altura_barra = 30
        colores = {}

        for item in historial:
            proceso_id = item['id']
            inicio = item['Inicio']
            fin = item['Fin']

            if proceso_id not in colores:
                colores[proceso_id] = utils.generar_color(proceso_id)

            x1 = (inicio - min_tiempo) * escala_x + 20
            x2 = (fin - min_tiempo) * escala_x + 20
            canvas.create_rectangle(x1, y_pos, x2, y_pos + altura_barra, fill=colores[proceso_id], outline="black")
            canvas.create_text((x1 + x2) / 2, y_pos + altura_barra / 2, text=proceso_id)

        # Métricas
        tabla_metricas = ttk.Treeview(ventana_resultados, columns=("id", "Espera", "Retorno", "Respuesta"))
        tabla_metricas.heading("#1", text="ID")
        tabla_metricas.heading("#2", text="Espera")
        tabla_metricas.heading("#3", text="Retorno")
        tabla_metricas.heading("#4", text="Respuesta")
        tabla_metricas.pack(pady=10)

        for i, proceso in enumerate(self.procesos):
            respuesta_val = round(respuesta[i], 2) if respuesta else "N/A"
            tabla_metricas.insert("", tk.END, values=(proceso['id'], round(espera[i], 2), round(retorno[i], 2), respuesta_val))

        promedio_espera = sum(espera) / len(espera) if espera else 0
        promedio_retorno = sum(retorno) / len(retorno) if retorno else 0
        promedio_respuesta = sum(respuesta) / len(respuesta) if respuesta else 0
        uso_cpu_str = f"{uso_cpu:.2f}%" if uso_cpu is not None else "N/A"

        ttk.Label(ventana_resultados, text=f"Promedio de Espera: {promedio_espera:.2f}").pack()
        ttk.Label(ventana_resultados, text=f"Promedio de Retorno: {promedio_retorno:.2f}").pack()
        ttk.Label(ventana_resultados, text=f"Promedio de Respuesta: {promedio_respuesta:.2f}").pack()
        ttk.Label(ventana_resultados, text=f"Uso de CPU: {uso_cpu_str}").pack()

    def actualizar_interfaz_quantum(self, *args):
        algoritmo = self.algoritmo_seleccionado.get()
        if algoritmo == "Round Robin":
            self.quantum_label.grid(row=1, column=0, padx=5, pady=5)
            self.quantum_entry.grid(row=1, column=1, padx=5, pady=5)
        else:
            self.quantum_label.grid_forget()
            self.quantum_entry.grid_forget()

if __name__ == "__main__":
    print("Entrando en el bloque if __name__ == '__main__':")
    root = tk.Tk()
    print("Ventana Tk creada.")
    app = SimuladorPlanificacion(root)
    print("Instancia de SimuladorPlanificacion creada.")

    # Botón para iniciar la simulación
    ttk.Button(root, text="Simular", command=app.simular).grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    root.mainloop()
    print("Bucle principal de Tkinter finalizado.")