import streamlit as st
import json
import os
from collections import defaultdict, Counter

json_file = 'jugadores.json'

def cargar_datos():
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            return json.load(file)
    return {}

def guardar_datos(datos):
    with open(json_file, 'w') as file:
        json.dump(datos, file, indent=4)

def clasificar_jugadores(jugadores):
    clasificaciones = {}
    clasificacion_texto = {
        '1': 'malo',
        '2': 'bueno',
        '3': 'excelente'
    }
    
    clasificaciones = {}
    for jugador in jugadores:
        clasificacion_num = st.selectbox(f"Clasifica a {jugador}", ['1', '2', '3'], key=jugador)
        clasificaciones[jugador] = clasificacion_texto[clasificacion_num]
    
    return clasificaciones

def agregar_jugadores():
    datos = cargar_datos()
    
    st.header("Agregar Jugadores")
    jugadores = []
    while True:
        jugador = st.text_input("Ingresa el nombre del jugador (deja vacío para terminar):")
        if not jugador:
            break
        jugadores.append(jugador.strip())
    
    clasificaciones = clasificar_jugadores(jugadores)
    
    if clasificaciones:
        for jugador in jugadores:
            if jugador in datos:
                datos[jugador]['clasificaciones'].append(clasificaciones[jugador])
            else:
                datos[jugador] = {
                    "estado": "Nuevo",
                    "clasificaciones": [clasificaciones[jugador]]
                }
        guardar_datos(datos)
        st.write("Datos actualizados:")
        for jugador, info in datos.items():
            st.write(f"{jugador}: {info}")

def consultar_jugadores():
    datos = cargar_datos()
    
    st.header("Consultar Jugadores")
    consulta = []
    while True:
        jugador = st.text_input("Ingresa el nombre del jugador (deja vacío para terminar):", key=f"consulta_{len(consulta)}")
        if not jugador:
            break
        consulta.append(jugador.strip())
    
    conteo_clasificaciones = defaultdict(Counter)
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
        st.write("Has jugado anteriormente con los siguientes jugadores:")
        for jugador in encontrados:
            conteos = conteo_clasificaciones[jugador]
            conteo_texto = ', '.join(f"{k.capitalize()}: {v}" for k, v in conteos.items())
            st.write(f"- {jugador} ({conteo_texto})")
    else:
        st.write("No has jugado anteriormente con ninguno de los jugadores consultados.")
    
    if no_encontrados:
        st.write("Estos jugadores no se encontraron en la lista:")
        for jugador in no_encontrados:
            st.write(f"- {jugador}")

def main():
    st.title("YA JUGUE CON ESE MANCO")  # Título principal
    st.markdown("---")  # Línea horizontal para separar el título del contenido
    
    opcion = st.selectbox("Selecciona una opción:", ["Agregar jugadores", "Consultar jugadores anteriores", "Salir"])
    
    if opcion == 'Agregar jugadores':
        agregar_jugadores()
    elif opcion == 'Consultar jugadores anteriores':
        consultar_jugadores()
    elif opcion == 'Salir':
        st.write("Saliendo...")

if __name__ == "__main__":
    main()
