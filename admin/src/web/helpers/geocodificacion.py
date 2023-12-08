from geopy.geocoders import Bing
from os import environ

def geocodificacion(direccion):
    """Funcion que retorna el link de un mapa de Bing con la direccion pasada por parámetro"""

    location = get_location(direccion + ", Argentina")

    if location is not None:
        return f"https://www.bing.com/maps/embed?h=400&w=600&cp={location.latitude}~{location.longitude}&lvl=15&typ=d&sty=r&src=SHELL&FORM=MBEDV8"
    else:
        print("La dirección no se pudo geocodificar")


def get_location(direccion):
    """Funcion que retorna la latitud y longitud de una direccion pasada por parámetro"""
    API_KEY = "Akbnaw1QB4DPlojnrlnB-iVsuZLqgM4CUMa7L-veYrbSsNPdXUFNMliQsO0kqfiO"
    geolocator = Bing(api_key=API_KEY, timeout=10)

    # Realiza la geocodificación
    location = geolocator.geocode(direccion + ", Argentina")

    return location

def get_coord_from_link(link):
    """Funcion que retorna la latitud y longitud de un link de Bing Maps"""
    lat = float(link.split("cp=")[1].split("&")[0].split("~")[0])
    lon = float(link.split("cp=")[1].split("&")[0].split("~")[1])

    return {"latitude": lat, "longitude": lon}