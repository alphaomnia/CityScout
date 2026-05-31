PRAGUE_BBOX = {"south": 49.9419, "west": 14.2244, "north": 50.1774, "east": 14.7072}
PRAGUE_CENTER = (50.0755, 14.4378)
PRAGUE_SEARCH_RADIUS_M = 15_000

PRAGUE_DISTRICTS = [f"Prague {i}" for i in range(1, 11)]
PRAGUE_NEIGHBORHOODS = [
    "Staré Město", "Nové Město", "Malá Strana", "Hradčany",
    "Vinohrady", "Žižkov", "Smíchov", "Holešovice",
    "Dejvice", "Nusle", "Vršovice", "Letná", "Bubeneč", "Pankrác",
]
NEIGHBORHOODS = PRAGUE_NEIGHBORHOODS  # backwards compat

BRNO_BBOX = {"south": 49.1200, "west": 16.4800, "north": 49.2700, "east": 16.7300}
BRNO_CENTER = (49.1951, 16.6068)
BRNO_SEARCH_RADIUS_M = 8_000

BRNO_DISTRICTS = [
    "Brno-střed", "Brno-sever", "Brno-jih", "Brno-Žabovřesky",
    "Brno-Židenice", "Brno-Vinohrady", "Brno-Královo Pole",
]
BRNO_NEIGHBORHOODS = [
    "Staré Brno", "Veveří", "Černá Pole", "Žabovřesky",
    "Židenice", "Husovice", "Líšeň", "Bohunice", "Štýršice",
]

CITIES = {
    "prague": {
        "name": "Prague",
        "bbox": PRAGUE_BBOX,
        "center": PRAGUE_CENTER,
        "radius_m": PRAGUE_SEARCH_RADIUS_M,
        "districts": PRAGUE_DISTRICTS,
        "neighborhoods": PRAGUE_NEIGHBORHOODS,
        "osm_name": "Praha",
    },
    "brno": {
        "name": "Brno",
        "bbox": BRNO_BBOX,
        "center": BRNO_CENTER,
        "radius_m": BRNO_SEARCH_RADIUS_M,
        "districts": BRNO_DISTRICTS,
        "neighborhoods": BRNO_NEIGHBORHOODS,
        "osm_name": "Brno",
    },
}

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
FOURSQUARE_BASE = "https://api.foursquare.com/v3"
GOOGLE_PLACES_BASE = "https://maps.googleapis.com/maps/api/place"

GOOGLE_DETAIL_FIELDS_BASIC = (
    "name,formatted_address,geometry,place_id,types,"
    "address_components,permanently_closed"
)
GOOGLE_DETAIL_FIELDS_CONTACT = "formatted_phone_number,website,opening_hours"
GOOGLE_DETAIL_FIELDS_ATMOSPHERE = "price_level,rating,user_ratings_total,photos"
