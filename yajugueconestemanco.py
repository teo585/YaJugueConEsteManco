import streamlit as st
import json
import os
from collections import defaultdict, Counter  # Importa Counter aquí
import re

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
    clasificacion_texto = {
        '1': 'malo',
        '2': 'bueno',
        '3': 'excelente',
        '4': 'troll',
        '5': 'afk'
    }
    
    clasificaciones = {}
    clasificaciones_opciones = [f"{numero}: {texto}" for numero, texto in clasificacion_texto.items()]
    
    for jugador in jugadores:
        clasificacion_opcion = st.selectbox(
            f"Clasifica a {jugador}", 
            options=clasificaciones_opciones, 
            key=f"clasificacion_{jugador}"
        )
        clasificacion_num = clasificacion_opcion.split(":")[0].strip()  # Extrae el número de la opción seleccionada
        clasificaciones[jugador] = clasificacion_texto[clasificacion_num]
    
    return clasificaciones

def procesar_texto_entrada(texto):
    jugadores = re.findall(r'⁦⁦(.*?)⁩', texto)
    return jugadores

def agregar_jugadores():
    datos = cargar_datos()
    
    st.header("Agregar Jugadores")
    
    st.warning("**IMPORTANTE:**  Asegúrate de ingresar tu nick exactamente. La búsqueda es sensible a mayúsculas y minúsculas.")
    
    # Pide el nick del usuario
    nick = st.text_input("Ingresa tu nick:")
    if not nick:
        st.warning("Debes ingresar un nick para continuar.")
        return
    
    # Pide el texto de entrada
    texto_entrada = st.text_area("Ingresa la lista de jugadores en formato de texto:")
    if not texto_entrada:
        st.warning("Debes ingresar el texto de los jugadores para continuar.")
        return
    
    jugadores = procesar_texto_entrada(texto_entrada)
    if not jugadores:
        st.warning("No se encontraron jugadores en el texto ingresado.")
        return
    
    # Mostrar opciones de clasificación para cada jugador
    clasificaciones = clasificar_jugadores(jugadores)
    
    if clasificaciones:
        # Inicializar datos para el nick si no existe
        if nick not in datos:
            datos[nick] = {"jugadores": {}}
        
        # Asegurarse de que la clave 'jugadores' esté presente
        if 'jugadores' not in datos[nick]:
            datos[nick]['jugadores'] = {}
        
        if st.button("Guardar Clasificaciones"):
            for jugador in jugadores:
                if jugador not in datos[nick]['jugadores']:
                    datos[nick]['jugadores'][jugador] = {
                        "estado": "Nuevo",
                        "clasificaciones": []
                    }
                datos[nick]['jugadores'][jugador]['clasificaciones'].append(clasificaciones[jugador])
            
            guardar_datos(datos)
            st.success("Datos actualizados y guardados exitosamente.")
            #st.write("Datos actualizados:")
            
            #for jugador, info in datos[nick]['jugadores'].items():
             #   st.write(f"{jugador}: {info}")

def consultar_jugadores():
    datos = cargar_datos()
    
    st.header("Consultar Jugadores")
    
    st.warning("**IMPORTANTE:** Asegúrate de ingresar tu nick exactamente. La búsqueda es sensible a mayúsculas y minúsculas.")
    
    # Pide el nick del usuario para la consulta
    nick = st.text_input("Ingresa tu nick para la consulta:")
    if not nick:
        st.warning("Debes ingresar tu nick para continuar.")
        return
    
    if nick not in datos:
        st.write("No se encontraron datos para el nick ingresado.")
        return
    
    # Pide el texto de entrada
    texto_entrada = st.text_area("Ingresa la lista de jugadores para consultar:")
    if not texto_entrada:
        st.warning("Debes ingresar el texto de los jugadores para consultar.")
        return
    
    consulta = procesar_texto_entrada(texto_entrada)
    if not consulta:
        st.warning("No se encontraron jugadores en el texto ingresado.")
        return
    
    conteo_clasificaciones = defaultdict(Counter)  # Esto ahora funcionará correctamente
    encontrados = []
    no_encontrados = []
    
    for jugador in consulta:
        if jugador in datos[nick]['jugadores']:
            encontrados.append(jugador)
            clasificaciones = datos[nick]['jugadores'][jugador]['clasificaciones']
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
    st.title("YA JUGUE CON ESE MANCO (BETA)")  # Título principal
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
