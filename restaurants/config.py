# Czech Republic
PRAGUE_BBOX = {"south": 49.9419, "west": 14.2244, "north": 50.1774, "east": 14.7072}
PRAGUE_CENTER = (50.0755, 14.4378)
PRAGUE_SEARCH_RADIUS_M = 15_000
PRAGUE_DISTRICTS = [f"Prague {i}" for i in range(1, 11)]
PRAGUE_NEIGHBORHOODS = [
    "Staré Město", "Nové Město", "Malá Strana", "Hradčany",
    "Vinohrady", "Žižkov", "Smíchov", "Holešovice",
    "Dejvice", "Nusle", "Vršovice", "Letná", "Bubeneč", "Pankrác",
]

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

# Slovakia
BRATISLAVA_BBOX = {"south": 48.0500, "west": 16.9500, "north": 48.2500, "east": 17.2800}
BRATISLAVA_CENTER = (48.1486, 17.1077)
BRATISLAVA_SEARCH_RADIUS_M = 8_000
BRATISLAVA_DISTRICTS = [
    "Bratislava I", "Bratislava II", "Bratislava III",
    "Bratislava IV", "Bratislava V",
]
BRATISLAVA_NEIGHBORHOODS = [
    "Staré Mesto", "Petržalka", "Ružinov", "Karlova Ves",
    "Nové Mesto", "Dúbravka", "Lamač", "Vajnory",
]

KOSICE_BBOX = {"south": 48.6700, "west": 21.1800, "north": 48.7800, "east": 21.3200}
KOSICE_CENTER = (48.7164, 21.2611)
KOSICE_SEARCH_RADIUS_M = 6_000
KOSICE_DISTRICTS = ["Košice I", "Košice II", "Košice III", "Košice IV"]
KOSICE_NEIGHBORHOODS = [
    "Staré Mesto", "Južné Mesto", "Sever", "Západ", "Dargovských hrdinov",
]

CITIES = {
    "prague": {
        "name": "Prague", "country": "Czech Republic",
        "bbox": PRAGUE_BBOX, "center": PRAGUE_CENTER, "radius_m": PRAGUE_SEARCH_RADIUS_M,
        "districts": PRAGUE_DISTRICTS, "neighborhoods": PRAGUE_NEIGHBORHOODS, "osm_name": "Praha",
    },
    "brno": {
        "name": "Brno", "country": "Czech Republic",
        "bbox": BRNO_BBOX, "center": BRNO_CENTER, "radius_m": BRNO_SEARCH_RADIUS_M,
        "districts": BRNO_DISTRICTS, "neighborhoods": BRNO_NEIGHBORHOODS, "osm_name": "Brno",
    },
    "bratislava": {
        "name": "Bratislava", "country": "Slovakia",
        "bbox": BRATISLAVA_BBOX, "center": BRATISLAVA_CENTER, "radius_m": BRATISLAVA_SEARCH_RADIUS_M,
        "districts": BRATISLAVA_DISTRICTS, "neighborhoods": BRATISLAVA_NEIGHBORHOODS, "osm_name": "Bratislava",
    },
    "kosice": {
        "name": "Košice", "country": "Slovakia",
        "bbox": KOSICE_BBOX, "center": KOSICE_CENTER, "radius_m": KOSICE_SEARCH_RADIUS_M,
        "districts": KOSICE_DISTRICTS, "neighborhoods": KOSICE_NEIGHBORHOODS, "osm_name": "Košice",
    },
}

# backwards compat
NEIGHBORHOODS = PRAGUE_NEIGHBORHOODS

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
FOURSQUARE_BASE = "https://api.foursquare.com/v3"
GOOGLE_PLACES_BASE = "https://maps.googleapis.com/maps/api/place"

GOOGLE_DETAIL_FIELDS_BASIC = (
    "name,formatted_address,geometry,place_id,types,"
    "address_components,permanently_closed"
)
GOOGLE_DETAIL_FIELDS_CONTACT = "formatted_phone_number,website,opening_hours"
GOOGLE_DETAIL_FIELDS_ATMOSPHERE = "price_level,rating,user_ratings_total,photos"
