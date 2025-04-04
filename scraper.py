import os
import requests
import pandas as pd

# Tu API Key de Google Places
API_KEY = os.environ.get('API_KEY')

# Coordenadas aproximadas de Bogotá
latitude = 4.7110
longitude = -74.0721
radius = 5000  # Radio de búsqueda en metros

# Termino de búsqueda: Cosméticos
#search_term = 'cosmetics'

# URL de Google Places para buscar lugares
places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Parámetros para la consulta de búsqueda
params = {
    'location': f'{latitude},{longitude}',
    'radius': radius,
    'type': 'store',
    #'keyword': search_term,
    'key': API_KEY
}

def obtener_url_busqueda_negocio(palabras_clave):
    p = params
    p['keyword'] = palabras_clave
    return requests.get(places_url, params=p).url

def obtener_comentarios(place_id):
    # URL para obtener los detalles del lugar, incluyendo los comentarios
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    details_params = {
        'place_id': place_id,
        'key': API_KEY,
        'reviews_no_translations': True
    }
    
    response = requests.get(details_url, params=details_params)
    #print(response.url)
    place_data = response.json()
    
    # Extraer comentarios si existen
    comments = []
    if 'result' in place_data and 'reviews' in place_data['result']:
        for review in place_data['result']['reviews']:
            comments.append({
                'author': review.get('author_name'),
                'rating': review.get('rating'),
                'text': review.get('text'),
                'time': review.get('time')
            })
    
    return comments

def obtener_negocios(palabras_clave):
    p = params
    p['keyword'] = palabras_clave
    return requests.get(places_url, params=p).json()

def buscar_negocios(palabras_clave):
    # Realizamos la solicitud a Google Places API
    '''params['keyword'] = palabras_clave
    response = requests.get(places_url, params=params)
    places_data = response.json()'''
    places_data = obtener_negocios(palabras_clave)
    '''json_object = json.dumps(places_data, indent=4)
    with open("response.json", "w") as outfile:
        outfile.write(json_object)'''
    rows = []
    
    if 'results' in places_data:
        for place in places_data['results']:
            p = dict()
            place_name = place['name']
            place_address = place.get('vicinity', 'No disponible')
            place_id = place['place_id']
            print(place_name)
            p['id'] = place_id
            p['name'] = place_name
            p['address'] = place_address
            p['comments'] = []
            # Obtener los comentarios de este negocio
            comentarios = obtener_comentarios(place_id)
            if comentarios:
                for comment in comentarios:
                    comment_data = {
                        'author': comment['author'],
                        'rating': comment['rating'],
                        'text': comment['text'],
                        'time': comment['time']
                    }
                    p['comments'].append(comment_data)
            rows.append(p)
            

    '''if 'results' in places_data:
        for place in places_data['results']:
            place_name = place['name']
            place_address = place.get('vicinity', 'No disponible')
            place_id = place['place_id']

            print(f"Nombre: {place_name}")
            print(f"Dirección: {place_address}")
            print("=" * 60)

            # Obtener los comentarios de este negocio
            comentarios = obtener_comentarios(place_id)
            if not comentarios:
                author = rating = text = ""
            else:
                for comment in comentarios:
                    author = comment['author']
                    rating = comment['rating']
                    text = comment['text']
                    rows.append({
                        'Nombre del lugar': place_name,
                        'Dirección': place_address,
                        'Autor': author,
                        'Calificación': rating,
                        'Comentario': text
                    })
    df = pd.DataFrame(rows)
    df.to_csv("reseñas.csv", index=False)
    print("Reseñas guardadas en reseñas.csv")'''
    return rows

#buscar_negocios("cosmetics")