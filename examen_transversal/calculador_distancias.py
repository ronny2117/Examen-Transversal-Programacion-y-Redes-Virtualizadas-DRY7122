#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopy.distance
import os
import sys
import subprocess
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def abrir_navegador(url):
    """Función especial para DevAsc que usa el navegador correcto"""
    try:
        # Intenta con el comando específico de DevAsc
        subprocess.run(["devasc-browser", url], check=True)
    except:
        try:
            # Fallback para sistemas normales
            webbrowser.open(url)
        except:
            print(f"\nNo se pudo abrir el navegador. Puede ver la ruta manualmente en:\n{url}")

def obtener_coordenadas(ciudad, pais):
    geolocator = Nominatim(user_agent="devasc_script")
    try:
        location = geolocator.geocode(f"{ciudad}, {pais}", timeout=10)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"\nNo se pudo encontrar {ciudad}, {pais}. Intente con un nombre más específico.")
            print("Ejemplos válidos: 'Santiago, Chile', 'Lima, Perú'")
            return None
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        print(f"\nError al conectar con el servicio de geocodificación: {e}")
        return None

def calcular_distancia(coord1, coord2):
    if coord1 and coord2:
        return geopy.distance.distance(coord1, coord2)
    return None

def mostrar_menu_transporte():
    print("\nSeleccione medio de transporte:")
    print("1. Automóvil (80 km/h)")
    print("2. Tren (120 km/h)")
    print("3. Avión (800 km/h)")
    print("0. Volver al menú principal")
    print("s. Salir del programa")
    return input("Opción: ").strip().lower()

def calcular_duracion(distancia_km, transporte):
    if transporte == "1":
        velocidad = 80
        medio = "en automóvil"
    elif transporte == "2":
        velocidad = 120
        medio = "en tren"
    elif transporte == "3":
        velocidad = 800
        medio = "en avión"
    else:
        return None
    
    horas = distancia_km / velocidad
    dias = int(horas // 24)
    horas_restantes = horas % 24
    
    return f"{dias} días y {horas_restantes:.1f} horas {medio}"

def generar_narrativa(origen, destino, distancia_km, duracion):
    return f"""\nNarrativa del viaje:
    Su viaje desde {origen} hasta {destino} será una aventura inolvidable.
    Recorrerá {distancia_km:.2f} km ({distancia_km*0.621371:.2f} millas),
    lo que tomará aproximadamente {duracion}.
    Prepare sus maletas y disfrute del paisaje durante este trayecto."""

def main():
    print("\n=== Calculador de Distancias Chile-Perú ===")
    
    while True:
        print("\nMenú principal:")
        print("1. Calcular distancia entre ciudades")
        print("s. Salir del programa")
        opcion = input("Seleccione una opción: ").strip().lower()
        
        if opcion == 's':
            print("\nSaliendo del programa...")
            sys.exit(0)
        elif opcion == '1':
            while True:
                origen = input("\nCiudad de Origen (Chile): ").strip()
                destino = input("Ciudad de Destino (Perú): ").strip()
                
                # Mejorar la entrada del usuario
                if not origen.lower().endswith("chile"):
                    origen += ", Chile"
                if not destino.lower().endswith("perú") and not destino.lower().endswith("peru"):
                    destino += ", Perú"
                
                coord_origen = obtener_coordenadas(origen, "Chile")
                coord_destino = obtener_coordenadas(destino, "Perú")
                
                if not coord_origen or not coord_destino:
                    break
                    
                distancia = calcular_distancia(coord_origen, coord_destino)
                if not distancia:
                    break
                    
                distancia_km = distancia.kilometers
                distancia_millas = distancia.miles
                
                while True:
                    transporte = mostrar_menu_transporte()
                    
                    if transporte == '0':
                        break
                    elif transporte == 's':
                        print("\nSaliendo del programa...")
                        sys.exit(0)
                    elif transporte not in ['1', '2', '3']:
                        print("\nOpción no válida. Intente nuevamente.")
                        continue
                        
                    duracion = calcular_duracion(distancia_km, transporte)
                    narrativa = generar_narrativa(origen, destino, distancia_km, duracion)
                    
                    print("\n=== Resultados ===")
                    print(f"Distancia en kilómetros: {distancia_km:.2f} km")
                    print(f"Distancia en millas: {distancia_millas:.2f} mi")
                    print(f"Duración del viaje: {duracion}")
                    print(narrativa)
                    
                    ver_mapa = input("\n¿Desea ver la ruta en el mapa? (s/n): ").strip().lower()
                    if ver_mapa == 's':
                        url = f"https://www.google.com/maps/dir/{coord_origen[0]},{coord_origen[1]}/{coord_destino[0]},{coord_destino[1]}"
                        abrir_navegador(url)
                    
                    otra_opcion = input("\n¿Desea probar otro medio de transporte? (s/n): ").strip().lower()
                    if otra_opcion != 's':
                        break
                break
        else:
            print("\nOpción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()