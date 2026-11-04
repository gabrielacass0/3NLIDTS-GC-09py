import tkinter as tk
from tkinter import messagebox
import serial
import time
import threading

# Configura el puerto y la velocidad de baudios para el Arduino
arduino_port = "COM3"  # Cambia esto al puerto donde esté tu Arduino
baud_rate = 9600
arduino = None  # Variable para la conexión serial

# Función para conectar al Arduino y enviar el límite de temperatura
def conectar():
    global arduino
    try:
        arduino = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)  # Espera para que se establezca la conexión
        lbConection.config(text="Estado: Conectado", fg="green")
        messagebox.showinfo("Conexión", "Conexión establecida.")
        start_reading()  # Inicia la lectura de datos en un hilo separado
    except serial.SerialException:
        messagebox.showerror("Error", "No se pudo conectar al Arduino. Verifique")

# Función para desconectar el Arduino
def desconectar():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
        lbConection.config(text="Estado: Desconectado", fg="red")
        messagebox.showinfo("Conexión", "Conexión terminada.")
    else:
        messagebox.showwarning("Advertencia", "No hay conexión activa.")

# Función para enviar el límite de temperatura al Arduino
def enviar_limite():
    global arduino
    if arduino and arduino.is_open:
        try:
            limite = tbLimTemp.get()
            if limite.isdigit():  # Verifica si el límite es un número válido
                arduino.write(f"{limite}\n".encode())  # Envía el límite al Arduino
                messagebox.showinfo("Enviado", f"Límite de temperatura ({limite}°C) enviado.")
            else:
                messagebox.showerror("Error", "Ingrese un valor numérico para el límite.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el límite: {e}")
    else:
        messagebox.showwarning("Advertencia", "Conéctese al Arduino antes de enviar el límite.")

# Función para leer datos desde el Arduino
def read_from_arduino():
    global arduino
    while arduino and arduino.is_open:
        try:
            data = arduino.readline().decode().strip()  # Lee los datos de temperatura
            if "Temperatura" in data:  # Filtra solo las líneas que contienen temperatura
                temp_value = data.split(":")[1].strip().split(" ")[0]
                lbTemp.config(text=f"{temp_value} °C")
                time.sleep(1)
        except Exception as e:
            print(f"Error Leyendo datos: {e}")
            break

# Función para iniciar la lectura en un hilo separado
def start_reading():
    thread = threading.Thread(target=read_from_arduino)
    thread.daemon = True
    thread.start()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Interfaz de Monitoreo de Temperatura")
root.geometry("300x350")

# Etiqueta de título de temperatura
lbTitleTemp = tk.Label(root, text="Temperatura Actual", font=("Arial", 12))
lbTitleTemp.pack(pady=10)

# Etiqueta para mostrar la temperatura
lbTemp = tk.Label(root, text="-- °C", font=("Arial", 24))
lbTemp.pack()

# Etiqueta de estado de conexión
lbConection = tk.Label(root, text="Estado: Desconectado", fg="red", font=("Arial", 10))
lbConection.pack(pady=5)

# Entrada para el límite de temperatura
lbLimitTemp = tk.Label(root, text="Límite de Temperatura:")
lbLimitTemp.pack(pady=5)
tbLimTemp = tk.Entry(root, width=10)
tbLimTemp.pack(pady=5)

# Botón para enviar el límite de temperatura
btnEnviar = tk.Button(root, text="Enviar Limite", command=enviar_limite, font=("Arial", 10))
btnEnviar.pack(pady=5)

# Botón de Conectar
btnConectar = tk.Button(root, text="Conectar", command=conectar, font=("Arial", 10))
btnConectar.pack(pady=5)

# Botón de Desconectar
btnDesconectar = tk.Button(root, text="Desconectar", command=desconectar, font=("Arial", 10))
btnDesconectar.pack(pady=5)

# Ejecuta la interfaz
root.mainloop()

