import json
import os
from collections import defaultdict, Counter

# Ruta del archivo JSON para almacenar la lista de jugadores
json_file = 'jugadores.json'

# Función para cargar datos desde el archivo JSON
def cargar_datos():
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    return {}

# Función para guardar datos en el archivo JSON
def guardar_datos(datos):
    with open(json_file, 'w') as file:
        json.dump(datos, file, indent=4)

# Función para clasificar jugadores con números
def clasificar_jugadores(jugadores):
    clasificaciones = {}
    clasificacion_texto = {
        '1': 'malo',
        '2': 'bueno',
        '3': 'excelente'
    }
    
    print("Clasificaciones:")
    print("1 - malo")
    print("2 - bueno")
    print("3 - excelente")
    
    for jugador in jugadores:
        while True:
            clasificacion_num = input(f"Clasifica a {jugador} (1, 2, 3): ").strip()
            if clasificacion_num in clasificacion_texto:
                clasificaciones[jugador] = clasificacion_texto[clasificacion_num]
                break
            else:
                print("Número de clasificación no válido. Por favor, ingresa 1, 2 o 3.")
    return clasificaciones

# Función para agregar jugadores a la lista
def agregar_jugadores():
    datos = cargar_datos()
    
    print("Ingresa la lista de jugadores que se han unido a la sala (finaliza con una línea vacía):")
    jugadores = []
    while True:
        entrada = input().strip()
        if not entrada:
            break
        jugador = entrada.split(' ')[0].strip('⁦⁦').strip('⁩')
        jugadores.append(jugador)
    
    # Clasificar jugadores
    clasificaciones = clasificar_jugadores(jugadores)
    
    # Añadir nuevos jugadores y actualizar clasificaciones
    for jugador in jugadores:
        if jugador in datos:
            datos[jugador]['clasificaciones'].append(clasificaciones[jugador])
        else:
            datos[jugador] = {
                "estado": "Nuevo",
                "clasificaciones": [clasificaciones[jugador]]
            }
    
    guardar_datos(datos)
    
    # Mostrar resultados
    for jugador, info in datos.items():
        print(f"{jugador}: {info}")

# Función para consultar jugadores anteriores
def consultar_jugadores():
    datos = cargar_datos()
    
    # Inicializar contadores de clasificación
    conteo_clasificaciones = defaultdict(Counter)
    
    print("Ingresa la lista de jugadores para consultar (finaliza con una línea vacía):")
    consulta = []
    while True:
        entrada = input().strip()
        if not entrada:
            break
        jugador = entrada.split(' ')[0].strip('⁦⁦').strip('⁩')
        consulta.append(jugador)
    
    encontrados = []
    no_encontrados = []
    
    for jugador in consulta:
        if jugador in datos:
            encontrados.append(jugador)
            clasificaciones = datos[jugador]['clasificaciones']
            conteo_clasificaciones[jugador] = Counter(clasificaciones)
        else:
            no_encontrados.append(jugador)
    
    if encontrados:
        print("Has jugado anteriormente con los siguientes jugadores:")
        for jugador in encontrados:
            conteos = conteo_clasificaciones[jugador]
            conteo_texto = ', '.join(f"{k.capitalize()}: {v}" for k, v in conteos.items())
            print(f"- {jugador} ({conteo_texto})")
    else:
        print("No has jugado anteriormente con ninguno de los jugadores consultados.")
    
    if no_encontrados:
        print("Estos jugadores no se encontraron en la lista:")
        for jugador in no_encontrados:
            print(f"- {jugador}")

def main():
    while True:
        print("\nOpciones:")
        print("1. Agregar jugadores")
        print("2. Consultar jugadores anteriores")
        print("3. Salir")
        opcion = input("Selecciona una opción (1, 2 o 3): ").strip()
        
        if opcion == '1':
            agregar_jugadores()
        elif opcion == '2':
            consultar_jugadores()
        elif opcion == '3':
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
