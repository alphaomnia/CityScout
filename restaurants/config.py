# ── Czech Republic ────────────────────────────────────────────────────────────
PRAGUE_BBOX = {"south": 49.9419, "west": 14.2244, "north": 50.1774, "east": 14.7072}
PRAGUE_CENTER = (50.0755, 14.4378)
PRAGUE_SEARCH_RADIUS_M = 15_000
PRAGUE_DISTRICTS = [f"Prague {i}" for i in range(1, 11)]
PRAGUE_NEIGHBORHOODS = [
    "Staré Město", "Nové Město", "Malá Strana", "Hradčany",
    "Vinohrady", "Žižkov", "Smíchov", "Holešovice",
    "Dejvice", "Nusle", "Vršovice", "Letná",
]

BRNO_BBOX = {"south": 49.1200, "west": 16.4800, "north": 49.2700, "east": 16.7300}
BRNO_CENTER = (49.1951, 16.6068)
BRNO_SEARCH_RADIUS_M = 8_000
BRNO_DISTRICTS = ["Brno-střed", "Brno-sever", "Brno-jih", "Brno-Žabovřesky", "Brno-Židenice", "Brno-Královo Pole"]
BRNO_NEIGHBORHOODS = ["Staré Brno", "Veveří", "Černá Pole", "Žabovřesky", "Židenice", "Husovice", "Líšeň"]

# ── Slovakia ──────────────────────────────────────────────────────────────────
BRATISLAVA_BBOX = {"south": 48.0500, "west": 16.9500, "north": 48.2500, "east": 17.2800}
BRATISLAVA_CENTER = (48.1486, 17.1077)
BRATISLAVA_SEARCH_RADIUS_M = 8_000
BRATISLAVA_DISTRICTS = ["Bratislava I", "Bratislava II", "Bratislava III", "Bratislava IV", "Bratislava V"]
BRATISLAVA_NEIGHBORHOODS = ["Staré Mesto", "Petržalka", "Ružinov", "Karlova Ves", "Nové Mesto", "Dúbravka"]

KOSICE_BBOX = {"south": 48.6700, "west": 21.1800, "north": 48.7800, "east": 21.3200}
KOSICE_CENTER = (48.7164, 21.2611)
KOSICE_SEARCH_RADIUS_M = 6_000
KOSICE_DISTRICTS = ["Košice I", "Košice II", "Košice III", "Košice IV"]
KOSICE_NEIGHBORHOODS = ["Staré Mesto", "Južné Mesto", "Sever", "Západ"]

# ── Germany ───────────────────────────────────────────────────────────────────
BERLIN_BBOX = {"south": 52.3382, "west": 13.0888, "north": 52.6755, "east": 13.7611}
BERLIN_CENTER = (52.5200, 13.4050)
BERLIN_SEARCH_RADIUS_M = 20_000
BERLIN_DISTRICTS = ["Mitte", "Prenzlauer Berg", "Friedrichshain", "Kreuzberg", "Neukölln", "Charlottenburg", "Schöneberg", "Mitte Berlin"]
BERLIN_NEIGHBORHOODS = ["Mitte", "Prenzlauer Berg", "Friedrichshain", "Kreuzberg", "Neukölln", "Charlottenburg", "Schöneberg", "Wedding", "Tempelhof"]

MUNICH_BBOX = {"south": 47.9700, "west": 11.3600, "north": 48.2500, "east": 11.7700}
MUNICH_CENTER = (48.1351, 11.5820)
MUNICH_SEARCH_RADIUS_M = 15_000
MUNICH_DISTRICTS = ["Altstadt-Lehel", "Maxvorstadt", "Schwabing", "Au-Haidhausen", "Neuhausen", "Bogenhausen"]
MUNICH_NEIGHBORHOODS = ["Altstadt", "Maxvorstadt", "Schwabing", "Haidhausen", "Neuhausen", "Glockenbachviertel", "Lehel"]

HAMBURG_BBOX = {"south": 53.3950, "west": 9.7300, "north": 53.7500, "east": 10.3200}
HAMBURG_CENTER = (53.5511, 9.9937)
HAMBURG_SEARCH_RADIUS_M = 18_000
HAMBURG_DISTRICTS = ["Hamburg-Mitte", "Altona", "Eimsbüttel", "Hamburg-Nord", "Wandsbek", "Bergedorf"]
HAMBURG_NEIGHBORHOODS = ["Altstadt", "HafenCity", "Altona", "Eimsbüttel", "Eppen​dorf", "Barmbek", "Ottensen"]

FRANKFURT_BBOX = {"south": 50.0150, "west": 8.4700, "north": 50.2270, "east": 8.8000}
FRANKFURT_CENTER = (50.1109, 8.6821)
FRANKFURT_SEARCH_RADIUS_M = 12_000
FRANKFURT_DISTRICTS = ["Innenstadt", "Sachsenhausen", "Bornheim", "Gallus", "Westend", "Nordend"]
FRANKFURT_NEIGHBORHOODS = ["Altstadt", "Sachsenhausen", "Bornheim", "Westend", "Nordend", "Sachsenhausen Nord"]

COLOGNE_BBOX = {"south": 50.8300, "west": 6.7700, "north": 51.0850, "east": 7.1600}
COLOGNE_CENTER = (50.9333, 6.9500)
COLOGNE_SEARCH_RADIUS_M = 13_000
COLOGNE_DISTRICTS = ["Innenstadt", "Ehrenfeld", "Nippes", "Lindenthal", "Rodenkirchen", "Mülheim"]
COLOGNE_NEIGHBORHOODS = ["Altstadt", "Ehrenfeld", "Nippes", "Lindenthal", "Deutz", "Sülz"]

STUTTGART_BBOX = {"south": 48.6900, "west": 9.0400, "north": 48.8600, "east": 9.3200}
STUTTGART_CENTER = (48.7758, 9.1829)
STUTTGART_SEARCH_RADIUS_M = 10_000
STUTTGART_DISTRICTS = ["Stuttgart-Mitte", "Stuttgart-Nord", "Stuttgart-Süd", "Stuttgart-West", "Stuttgart-Ost"]
STUTTGART_NEIGHBORHOODS = ["Mitte", "Bad Cannstatt", "Vaihingen", "Degerloch", "Zuffenhausen"]

DUSSELDORF_BBOX = {"south": 51.1200, "west": 6.6700, "north": 51.3700, "east": 6.9000}
DUSSELDORF_CENTER = (51.2217, 6.7762)
DUSSELDORF_SEARCH_RADIUS_M = 10_000
DUSSELDORF_DISTRICTS = ["Stadtmitte", "Pempelfort", "Carlstadt", "Flingern", "Bilk", "Oberbilk"]
DUSSELDORF_NEIGHBORHOODS = ["Altstadt", "Carlstadt", "Pempelfort", "Flingern", "Bilk", "Friedrichstadt"]

# ── Austria ───────────────────────────────────────────────────────────────────
VIENNA_BBOX = {"south": 48.1177, "west": 16.1827, "north": 48.3228, "east": 16.5777}
VIENNA_CENTER = (48.2082, 16.3738)
VIENNA_SEARCH_RADIUS_M = 15_000
VIENNA_DISTRICTS = [f"Wien {i}. Bezirk" for i in range(1, 10)]
VIENNA_NEIGHBORHOODS = ["Innere Stadt", "Leopoldstadt", "Landstraße", "Wieden", "Mariahilf", "Naschmarkt", "Neubau", "Josefstadt", "Alsergrund"]

GRAZ_BBOX = {"south": 46.9900, "west": 15.3300, "north": 47.1300, "east": 15.5600}
GRAZ_CENTER = (47.0707, 15.4395)
GRAZ_SEARCH_RADIUS_M = 8_000
GRAZ_DISTRICTS = ["Graz-Innere Stadt", "Graz-Jakomini", "Graz-Geidorf", "Graz-Lend", "Graz-Eggenberg"]
GRAZ_NEIGHBORHOODS = ["Innere Stadt", "Jakomini", "Geidorf", "Lend", "Eggenberg"]

SALZBURG_BBOX = {"south": 47.7600, "west": 12.9800, "north": 47.8600, "east": 13.1300}
SALZBURG_CENTER = (47.8095, 13.0550)
SALZBURG_SEARCH_RADIUS_M = 6_000
SALZBURG_DISTRICTS = ["Altstadt", "Schallmoos", "Maxglan", "Lehen", "Nonntal"]
SALZBURG_NEIGHBORHOODS = ["Altstadt", "Schallmoos", "Maxglan", "Lehen", "Nonntal"]

INNSBRUCK_BBOX = {"south": 47.2300, "west": 11.3200, "north": 47.3200, "east": 11.5000}
INNSBRUCK_CENTER = (47.2692, 11.4041)
INNSBRUCK_SEARCH_RADIUS_M = 6_000
INNSBRUCK_DISTRICTS = ["Innere Stadt", "Wilten", "Pradl", "Hötting", "Saggen"]
INNSBRUCK_NEIGHBORHOODS = ["Innere Stadt", "Wilten", "Pradl", "Hötting", "Saggen"]

# ── Italy ─────────────────────────────────────────────────────────────────────
ROME_BBOX = {"south": 41.7600, "west": 12.3100, "north": 42.0400, "east": 12.6300}
ROME_CENTER = (41.9028, 12.4964)
ROME_SEARCH_RADIUS_M = 18_000
ROME_DISTRICTS = ["Centro Storico", "Trastevere", "Prati", "Testaccio", "Pigneto", "Parioli", "Ostiense", "Esquilino"]
ROME_NEIGHBORHOODS = ["Trastevere", "Prati", "Testaccio", "Pigneto", "Parioli", "Ostiense", "Monti", "Esquilino", "Garbatella"]

MILAN_BBOX = {"south": 45.3800, "west": 9.0500, "north": 45.5500, "east": 9.3200}
MILAN_CENTER = (45.4654, 9.1859)
MILAN_SEARCH_RADIUS_M = 12_000
MILAN_DISTRICTS = ["Centro", "Navigli", "Brera", "Isola", "Porta Romana", "Porta Venezia", "Sempione"]
MILAN_NEIGHBORHOODS = ["Navigli", "Brera", "Isola", "Porta Romana", "Porta Venezia", "Ticinese", "Sempione", "Cinque Vie"]

FLORENCE_BBOX = {"south": 43.7200, "west": 11.1800, "north": 43.8400, "east": 11.3500}
FLORENCE_CENTER = (43.7696, 11.2558)
FLORENCE_SEARCH_RADIUS_M = 8_000
FLORENCE_DISTRICTS = ["Centro Storico", "Oltrarno", "Santa Croce", "San Lorenzo", "Rifredi"]
FLORENCE_NEIGHBORHOODS = ["Oltrarno", "Santa Croce", "San Lorenzo", "Santo Spirito", "Duomo"]

VENICE_BBOX = {"south": 45.3900, "west": 12.2200, "north": 45.5000, "east": 12.4000}
VENICE_CENTER = (45.4408, 12.3155)
VENICE_SEARCH_RADIUS_M = 8_000
VENICE_DISTRICTS = ["San Marco", "Dorsoduro", "San Polo", "Santa Croce", "Cannaregio", "Castello"]
VENICE_NEIGHBORHOODS = ["San Marco", "Dorsoduro", "San Polo", "Cannaregio", "Castello", "Rialto"]

NAPLES_BBOX = {"south": 40.7900, "west": 14.1800, "north": 40.9200, "east": 14.3700}
NAPLES_CENTER = (40.8518, 14.2681)
NAPLES_SEARCH_RADIUS_M = 10_000
NAPLES_DISTRICTS = ["Centro Storico", "Chiaia", "Posillipo", "Vomero", "Fuorigrotta"]
NAPLES_NEIGHBORHOODS = ["Centro Storico", "Chiaia", "Posillipo", "Vomero", "Quartieri Spagnoli"]

BOLOGNA_BBOX = {"south": 44.4500, "west": 11.2700, "north": 44.5500, "east": 11.4300}
BOLOGNA_CENTER = (44.4949, 11.3426)
BOLOGNA_SEARCH_RADIUS_M = 7_000
BOLOGNA_DISTRICTS = ["Centro Storico", "Porto-Saragozza", "Navile", "San Donato", "Savena"]
BOLOGNA_NEIGHBORHOODS = ["Centro Storico", "Bolognina", "Saragozza", "Santo Stefano", "Irnerio"]

TURIN_BBOX = {"south": 44.9900, "west": 7.5900, "north": 45.1600, "east": 7.8200}
TURIN_CENTER = (45.0703, 7.6869)
TURIN_SEARCH_RADIUS_M = 10_000
TURIN_DISTRICTS = ["Centro", "Crocetta", "San Salvario", "Vàuchiglia", "Borgo Po"]
TURIN_NEIGHBORHOODS = ["Centro", "San Salvario", "Crocetta", "Aurora", "Vanchiglia", "Quadrilatero Romano"]

# ── Malta ─────────────────────────────────────────────────────────────────────
MALTA_BBOX = {"south": 35.7850, "west": 14.1790, "north": 36.0820, "east": 14.5770}
MALTA_CENTER = (35.9375, 14.3754)
MALTA_SEARCH_RADIUS_M = 20_000
MALTA_DISTRICTS = ["Valletta", "St Julian's", "Sliema", "Mdina", "Marsaxlokk", "Birgu"]
MALTA_NEIGHBORHOODS = ["Valletta", "St Julian's", "Sliema", "Mdina", "Marsaxlokk", "Birgu", "Rabat", "Mosta"]

# ── Netherlands ───────────────────────────────────────────────────────────────
AMSTERDAM_BBOX = {"south": 52.2900, "west": 4.7200, "north": 52.4300, "east": 5.1000}
AMSTERDAM_CENTER = (52.3676, 4.9041)
AMSTERDAM_SEARCH_RADIUS_M = 12_000
AMSTERDAM_DISTRICTS = ["Centrum", "De Pijp", "Jordaan", "Oost", "Noord", "West", "Oud-Zuid"]
AMSTERDAM_NEIGHBORHOODS = ["Centrum", "De Pijp", "Jordaan", "Oud-Zuid", "Plantage", "De Baarsjes", "Westerpark"]

ROTTERDAM_BBOX = {"south": 51.8600, "west": 4.3700, "north": 51.9800, "east": 4.6000}
ROTTERDAM_CENTER = (51.9225, 4.4792)
ROTTERDAM_SEARCH_RADIUS_M = 10_000
ROTTERDAM_DISTRICTS = ["Centrum", "Kralingen", "Delfshaven", "Noord", "Feijenoord"]
ROTTERDAM_NEIGHBORHOODS = ["Centrum", "Kralingen", "Delfshaven", "Hillegersberg", "Cool"]

THE_HAGUE_BBOX = {"south": 52.0100, "west": 4.2000, "north": 52.1500, "east": 4.4200}
THE_HAGUE_CENTER = (52.0705, 4.3007)
THE_HAGUE_SEARCH_RADIUS_M = 8_000
THE_HAGUE_DISTRICTS = ["Centrum", "Scheveningen", "Benoordenhout", "Segbroek", "Loosduinen"]
THE_HAGUE_NEIGHBORHOODS = ["Centrum", "Scheveningen", "Benoordenhout", "Statenkwartier", "Laak"]

UTRECHT_BBOX = {"south": 52.0500, "west": 5.0400, "north": 52.1500, "east": 5.2000}
UTRECHT_CENTER = (52.0907, 5.1214)
UTRECHT_SEARCH_RADIUS_M = 7_000
UTRECHT_DISTRICTS = ["Binnenstad", "Oost", "West", "Noord", "Zuid"]
UTRECHT_NEIGHBORHOODS = ["Binnenstad", "Wittevrouwen", "Lombok", "Zuilen", "Overvecht"]

# ── Denmark ───────────────────────────────────────────────────────────────────
COPENHAGEN_BBOX = {"south": 55.6100, "west": 12.4500, "north": 55.7500, "east": 12.7000}
COPENHAGEN_CENTER = (55.6761, 12.5683)
COPENHAGEN_SEARCH_RADIUS_M = 10_000
COPENHAGEN_DISTRICTS = ["Indre By", "Vesterbro", "Nørrebro", "Frederiksberg", "sterbro", "Christianshavn"]
COPENHAGEN_NEIGHBORHOODS = ["Indre By", "Vesterbro", "Nørrebro", "Frederiksberg", "sterbro", "Christianshavn", "Amagerbro"]

AARHUS_BBOX = {"south": 56.1100, "west": 10.1200, "north": 56.2100, "east": 10.3000}
AARHUS_CENTER = (56.1629, 10.2039)
AARHUS_SEARCH_RADIUS_M = 7_000
AARHUS_DISTRICTS = ["Midtbyen", "Trøjborg", "Frederiksbjerg", "Risskov", "Brabrand"]
AARHUS_NEIGHBORHOODS = ["Midtbyen", "Trøjborg", "Frederiksbjerg", "Christiansbjerg", "Åbyhøj"]

# ── Spain ─────────────────────────────────────────────────────────────────────
MADRID_BBOX = {"south": 40.3000, "west": -3.8800, "north": 40.5600, "east": -3.5200}
MADRID_CENTER = (40.4168, -3.7038)
MADRID_SEARCH_RADIUS_M = 18_000
MADRID_DISTRICTS = ["Centro", "Malasaña", "Chueca", "La Latina", "Lavarés", "Salamanca", "Retiro", "Chambertí"]
MADRID_NEIGHBORHOODS = ["Malasaña", "Chueca", "La Latina", "Lavarés", "Salamanca", "Sol", "Opera", "Huertas", "Chambertí"]

BARCELONA_BBOX = {"south": 41.3200, "west": 2.0500, "north": 41.4700, "east": 2.3000}
BARCELONA_CENTER = (41.3851, 2.1734)
BARCELONA_SEARCH_RADIUS_M = 12_000
BARCELONA_DISTRICTS = ["Ciutat Vella", "Eixample", "Gràcia", "Sant Pere", "El Born", "Barceloneta", "Poble Sec"]
BARCELONA_NEIGHBORHOODS = ["El Born", "Gràcia", "Eixample", "Barceloneta", "Poble Sec", "Raval", "Gòtic", "Poblenou"]

SEVILLE_BBOX = {"south": 37.3200, "west": -6.0900, "north": 37.4700, "east": -5.9000}
SEVILLE_CENTER = (37.3891, -5.9845)
SEVILLE_SEARCH_RADIUS_M = 8_000
SEVILLE_DISTRICTS = ["Casco Antiguo", "Triana", "La Macarena", "Los Remedios", "Nervion"]
SEVILLE_NEIGHBORHOODS = ["Casco Antiguo", "Triana", "La Macarena", "Los Remedios", "Nervion", "Santa Cruz"]

VALENCIA_BBOX = {"south": 39.4000, "west": -0.4700, "north": 39.5400, "east": -0.2800}
VALENCIA_CENTER = (39.4699, -0.3763)
VALENCIA_SEARCH_RADIUS_M = 9_000
VALENCIA_DISTRICTS = ["Ciutat Vella", "L'Eixample", "Extramurs", "Campanar", "La Saïdia"]
VALENCIA_NEIGHBORHOODS = ["Ciutat Vella", "Russafa", "El Carmen", "Benimaclet", "Ruzafa", "La Xerea"]

BILBAO_BBOX = {"south": 43.2200, "west": -3.0200, "north": 43.3300, "east": -2.8500}
BILBAO_CENTER = (43.2630, -2.9350)
BILBAO_SEARCH_RADIUS_M = 6_000
BILBAO_DISTRICTS = ["Casco Viejo", "Abando", "Indautxu", "Begoña", "Rekalde"]
BILBAO_NEIGHBORHOODS = ["Casco Viejo", "Abando", "Indautxu", "Begoña", "Rekalde"]

MALAGA_BBOX = {"south": 36.6700, "west": -4.5200, "north": 36.7700, "east": -4.3200}
MALAGA_CENTER = (36.7213, -4.4214)
MALAGA_SEARCH_RADIUS_M = 7_000
MALAGA_DISTRICTS = ["Centro", "La Malagueta", "Soho", "El Palo", "Pedregalejo"]
MALAGA_NEIGHBORHOODS = ["Centro", "La Malagueta", "Soho", "El Palo", "Pedregalejo", "Lagunillas"]

# ── Portugal ──────────────────────────────────────────────────────────────────
LISBON_BBOX = {"south": 38.6600, "west": -9.2300, "north": 38.7900, "east": -9.0800}
LISBON_CENTER = (38.7223, -9.1393)
LISBON_SEARCH_RADIUS_M = 10_000
LISBON_DISTRICTS = ["Baixa", "Alfama", "Bairro Alto", "Belém", "Mouraria", "LX Factory", "Principe Real", "Intendente"]
LISBON_NEIGHBORHOODS = ["Alfama", "Bairro Alto", "Belém", "Mouraria", "Principe Real", "Intendente", "Santos", "Chiado", "Graca"]

PORTO_BBOX = {"south": 41.1000, "west": -8.7200, "north": 41.2200, "east": -8.5500}
PORTO_CENTER = (41.1579, -8.6291)
PORTO_SEARCH_RADIUS_M = 9_000
PORTO_DISTRICTS = ["Baixa", "Ribeira", "Bonfim", "Cedofeita", "Foz do Douro", "Massarelos"]
PORTO_NEIGHBORHOODS = ["Ribeira", "Bonfim", "Cedofeita", "Foz do Douro", "Massarelos", "Miragaia", "Fontainhas"]

FARO_BBOX = {"south": 36.9800, "west": -8.0000, "north": 37.0700, "east": -7.8700}
FARO_CENTER = (37.0194, -7.9322)
FARO_SEARCH_RADIUS_M = 5_000
FARO_DISTRICTS = ["Cidade Velha", "Centro", "Montenegro", "São Pedro"]
FARO_NEIGHBORHOODS = ["Cidade Velha", "Centro", "Montenegro", "São Pedro"]

# ── Poland ────────────────────────────────────────────────────────────────────
WARSAW_BBOX = {"south": 52.0700, "west": 20.8500, "north": 52.3700, "east": 21.2100}
WARSAW_CENTER = (52.2297, 21.0122)
WARSAW_SEARCH_RADIUS_M = 18_000
WARSAW_DISTRICTS = ["Śródmieście", "Praga-Południe", "Wola", "Mokotów", "Żoliborz", "Ochota", "Ursynów"]
WARSAW_NEIGHBORHOODS = ["Śródmieście", "Praga", "Wola", "Mokotów", "Żoliborz", "Ochota", "Powiśle", "Stare Miasto"]

KRAKOW_BBOX = {"south": 49.9700, "west": 19.7900, "north": 50.1100, "east": 20.0800}
KRAKOW_CENTER = (50.0647, 19.9450)
KRAKOW_SEARCH_RADIUS_M = 12_000
KRAKOW_DISTRICTS = ["Stare Miasto", "Kazimierz", "Podgórze", "Krowodrza", "Nowa Huta"]
KRAKOW_NEIGHBORHOODS = ["Stare Miasto", "Kazimierz", "Podgórze", "Krowodrza", "Zwierzyniec", "Grzegórzki"]

WROCLAW_BBOX = {"south": 51.0100, "west": 16.8700, "north": 51.2000, "east": 17.2000}
WROCLAW_CENTER = (51.1079, 17.0385)
WROCLAW_SEARCH_RADIUS_M = 12_000
WROCLAW_DISTRICTS = ["Stare Miasto", "Śródmieście", "Krzyki", "Fabryczna", "Psie Pole"]
WROCLAW_NEIGHBORHOODS = ["Stare Miasto", "Nadodrze", "Ołbin", "Krzyki", "Przedmieście Świdnickie"]

GDANSK_BBOX = {"south": 54.2800, "west": 18.5200, "north": 54.4300, "east": 18.8100}
GDANSK_CENTER = (54.3520, 18.6466)
GDANSK_SEARCH_RADIUS_M = 9_000
GDANSK_DISTRICTS = ["Śródmieście", "Wrzeszcz", "Oliwa", "Nowy Port", "Zaspa"]
GDANSK_NEIGHBORHOODS = ["Śródmieście", "Wrzeszcz", "Oliwa", "Nowy Port", "Stare Miasto"]

POZNAN_BBOX = {"south": 52.3300, "west": 16.8000, "north": 52.5000, "east": 17.0700}
POZNAN_CENTER = (52.4064, 16.9252)
POZNAN_SEARCH_RADIUS_M = 10_000
POZNAN_DISTRICTS = ["Stare Miasto", "Grunwald", "Nowe Miasto", "Jeżyce", "Wilda"]
POZNAN_NEIGHBORHOODS = ["Stare Miasto", "Jeżyce", "Grunwald", "Wilda", "Łazarz"]

# ── CITIES registry ───────────────────────────────────────────────────────────
CITIES = {
    # Czech Republic
    "prague":      {"name": "Prague",      "country": "Czech Republic", "bbox": PRAGUE_BBOX,      "center": PRAGUE_CENTER,      "radius_m": PRAGUE_SEARCH_RADIUS_M,      "districts": PRAGUE_DISTRICTS,      "neighborhoods": PRAGUE_NEIGHBORHOODS,      "osm_name": "Praha"},
    "brno":        {"name": "Brno",        "country": "Czech Republic", "bbox": BRNO_BBOX,        "center": BRNO_CENTER,        "radius_m": BRNO_SEARCH_RADIUS_M,        "districts": BRNO_DISTRICTS,        "neighborhoods": BRNO_NEIGHBORHOODS,        "osm_name": "Brno"},
    # Slovakia
    "bratislava":  {"name": "Bratislava",  "country": "Slovakia",       "bbox": BRATISLAVA_BBOX,  "center": BRATISLAVA_CENTER,  "radius_m": BRATISLAVA_SEARCH_RADIUS_M,  "districts": BRATISLAVA_DISTRICTS,  "neighborhoods": BRATISLAVA_NEIGHBORHOODS,  "osm_name": "Bratislava"},
    "kosice":      {"name": "Košice",      "country": "Slovakia",       "bbox": KOSICE_BBOX,      "center": KOSICE_CENTER,      "radius_m": KOSICE_SEARCH_RADIUS_M,      "districts": KOSICE_DISTRICTS,      "neighborhoods": KOSICE_NEIGHBORHOODS,      "osm_name": "Košice"},
    # Germany
    "berlin":      {"name": "Berlin",      "country": "Germany",        "bbox": BERLIN_BBOX,      "center": BERLIN_CENTER,      "radius_m": BERLIN_SEARCH_RADIUS_M,      "districts": BERLIN_DISTRICTS,      "neighborhoods": BERLIN_NEIGHBORHOODS,      "osm_name": "Berlin"},
    "munich":      {"name": "Munich",      "country": "Germany",        "bbox": MUNICH_BBOX,      "center": MUNICH_CENTER,      "radius_m": MUNICH_SEARCH_RADIUS_M,      "districts": MUNICH_DISTRICTS,      "neighborhoods": MUNICH_NEIGHBORHOODS,      "osm_name": "München"},
    "hamburg":     {"name": "Hamburg",     "country": "Germany",        "bbox": HAMBURG_BBOX,     "center": HAMBURG_CENTER,     "radius_m": HAMBURG_SEARCH_RADIUS_M,     "districts": HAMBURG_DISTRICTS,     "neighborhoods": HAMBURG_NEIGHBORHOODS,     "osm_name": "Hamburg"},
    "frankfurt":   {"name": "Frankfurt",   "country": "Germany",        "bbox": FRANKFURT_BBOX,   "center": FRANKFURT_CENTER,   "radius_m": FRANKFURT_SEARCH_RADIUS_M,   "districts": FRANKFURT_DISTRICTS,   "neighborhoods": FRANKFURT_NEIGHBORHOODS,   "osm_name": "Frankfurt am Main"},
    "cologne":     {"name": "Cologne",     "country": "Germany",        "bbox": COLOGNE_BBOX,     "center": COLOGNE_CENTER,     "radius_m": COLOGNE_SEARCH_RADIUS_M,     "districts": COLOGNE_DISTRICTS,     "neighborhoods": COLOGNE_NEIGHBORHOODS,     "osm_name": "Köln"},
    "stuttgart":   {"name": "Stuttgart",   "country": "Germany",        "bbox": STUTTGART_BBOX,   "center": STUTTGART_CENTER,   "radius_m": STUTTGART_SEARCH_RADIUS_M,   "districts": STUTTGART_DISTRICTS,   "neighborhoods": STUTTGART_NEIGHBORHOODS,   "osm_name": "Stuttgart"},
    "dusseldorf":  {"name": "Düsseldorf",  "country": "Germany",        "bbox": DUSSELDORF_BBOX,  "center": DUSSELDORF_CENTER,  "radius_m": DUSSELDORF_SEARCH_RADIUS_M,  "districts": DUSSELDORF_DISTRICTS,  "neighborhoods": DUSSELDORF_NEIGHBORHOODS,  "osm_name": "Düsseldorf"},
    # Austria
    "vienna":      {"name": "Vienna",      "country": "Austria",        "bbox": VIENNA_BBOX,      "center": VIENNA_CENTER,      "radius_m": VIENNA_SEARCH_RADIUS_M,      "districts": VIENNA_DISTRICTS,      "neighborhoods": VIENNA_NEIGHBORHOODS,      "osm_name": "Wien"},
    "graz":        {"name": "Graz",        "country": "Austria",        "bbox": GRAZ_BBOX,        "center": GRAZ_CENTER,        "radius_m": GRAZ_SEARCH_RADIUS_M,        "districts": GRAZ_DISTRICTS,        "neighborhoods": GRAZ_NEIGHBORHOODS,        "osm_name": "Graz"},
    "salzburg":    {"name": "Salzburg",    "country": "Austria",        "bbox": SALZBURG_BBOX,    "center": SALZBURG_CENTER,    "radius_m": SALZBURG_SEARCH_RADIUS_M,    "districts": SALZBURG_DISTRICTS,    "neighborhoods": SALZBURG_NEIGHBORHOODS,    "osm_name": "Salzburg"},
    "innsbruck":   {"name": "Innsbruck",   "country": "Austria",        "bbox": INNSBRUCK_BBOX,   "center": INNSBRUCK_CENTER,   "radius_m": INNSBRUCK_SEARCH_RADIUS_M,   "districts": INNSBRUCK_DISTRICTS,   "neighborhoods": INNSBRUCK_NEIGHBORHOODS,   "osm_name": "Innsbruck"},
    # Italy
    "rome":        {"name": "Rome",        "country": "Italy",          "bbox": ROME_BBOX,        "center": ROME_CENTER,        "radius_m": ROME_SEARCH_RADIUS_M,        "districts": ROME_DISTRICTS,        "neighborhoods": ROME_NEIGHBORHOODS,        "osm_name": "Roma"},
    "milan":       {"name": "Milan",       "country": "Italy",          "bbox": MILAN_BBOX,       "center": MILAN_CENTER,       "radius_m": MILAN_SEARCH_RADIUS_M,       "districts": MILAN_DISTRICTS,       "neighborhoods": MILAN_NEIGHBORHOODS,       "osm_name": "Milano"},
    "florence":    {"name": "Florence",    "country": "Italy",          "bbox": FLORENCE_BBOX,    "center": FLORENCE_CENTER,    "radius_m": FLORENCE_SEARCH_RADIUS_M,    "districts": FLORENCE_DISTRICTS,    "neighborhoods": FLORENCE_NEIGHBORHOODS,    "osm_name": "Firenze"},
    "venice":      {"name": "Venice",      "country": "Italy",          "bbox": VENICE_BBOX,      "center": VENICE_CENTER,      "radius_m": VENICE_SEARCH_RADIUS_M,      "districts": VENICE_DISTRICTS,      "neighborhoods": VENICE_NEIGHBORHOODS,      "osm_name": "Venezia"},
    "naples":      {"name": "Naples",      "country": "Italy",          "bbox": NAPLES_BBOX,      "center": NAPLES_CENTER,      "radius_m": NAPLES_SEARCH_RADIUS_M,      "districts": NAPLES_DISTRICTS,      "neighborhoods": NAPLES_NEIGHBORHOODS,      "osm_name": "Napoli"},
    "bologna":     {"name": "Bologna",     "country": "Italy",          "bbox": BOLOGNA_BBOX,     "center": BOLOGNA_CENTER,     "radius_m": BOLOGNA_SEARCH_RADIUS_M,     "districts": BOLOGNA_DISTRICTS,     "neighborhoods": BOLOGNA_NEIGHBORHOODS,     "osm_name": "Bologna"},
    "turin":       {"name": "Turin",       "country": "Italy",          "bbox": TURIN_BBOX,       "center": TURIN_CENTER,       "radius_m": TURIN_SEARCH_RADIUS_M,       "districts": TURIN_DISTRICTS,       "neighborhoods": TURIN_NEIGHBORHOODS,       "osm_name": "Torino"},
    # Malta
    "malta":       {"name": "Malta",       "country": "Malta",          "bbox": MALTA_BBOX,       "center": MALTA_CENTER,       "radius_m": MALTA_SEARCH_RADIUS_M,       "districts": MALTA_DISTRICTS,       "neighborhoods": MALTA_NEIGHBORHOODS,       "osm_name": "Malta"},
    # Netherlands
    "amsterdam":   {"name": "Amsterdam",   "country": "Netherlands",    "bbox": AMSTERDAM_BBOX,   "center": AMSTERDAM_CENTER,   "radius_m": AMSTERDAM_SEARCH_RADIUS_M,   "districts": AMSTERDAM_DISTRICTS,   "neighborhoods": AMSTERDAM_NEIGHBORHOODS,   "osm_name": "Amsterdam"},
    "rotterdam":   {"name": "Rotterdam",   "country": "Netherlands",    "bbox": ROTTERDAM_BBOX,   "center": ROTTERDAM_CENTER,   "radius_m": ROTTERDAM_SEARCH_RADIUS_M,   "districts": ROTTERDAM_DISTRICTS,   "neighborhoods": ROTTERDAM_NEIGHBORHOODS,   "osm_name": "Rotterdam"},
    "the_hague":   {"name": "The Hague",   "country": "Netherlands",    "bbox": THE_HAGUE_BBOX,   "center": THE_HAGUE_CENTER,   "radius_m": THE_HAGUE_SEARCH_RADIUS_M,   "districts": THE_HAGUE_DISTRICTS,   "neighborhoods": THE_HAGUE_NEIGHBORHOODS,   "osm_name": "Den Haag"},
    "utrecht":     {"name": "Utrecht",     "country": "Netherlands",    "bbox": UTRECHT_BBOX,     "center": UTRECHT_CENTER,     "radius_m": UTRECHT_SEARCH_RADIUS_M,     "districts": UTRECHT_DISTRICTS,     "neighborhoods": UTRECHT_NEIGHBORHOODS,     "osm_name": "Utrecht"},
    # Denmark
    "copenhagen":  {"name": "Copenhagen",  "country": "Denmark",        "bbox": COPENHAGEN_BBOX,  "center": COPENHAGEN_CENTER,  "radius_m": COPENHAGEN_SEARCH_RADIUS_M,  "districts": COPENHAGEN_DISTRICTS,  "neighborhoods": COPENHAGEN_NEIGHBORHOODS,  "osm_name": "København"},
    "aarhus":      {"name": "Aarhus",      "country": "Denmark",        "bbox": AARHUS_BBOX,      "center": AARHUS_CENTER,      "radius_m": AARHUS_SEARCH_RADIUS_M,      "districts": AARHUS_DISTRICTS,      "neighborhoods": AARHUS_NEIGHBORHOODS,      "osm_name": "Aarhus"},
    # Spain
    "madrid":      {"name": "Madrid",      "country": "Spain",          "bbox": MADRID_BBOX,      "center": MADRID_CENTER,      "radius_m": MADRID_SEARCH_RADIUS_M,      "districts": MADRID_DISTRICTS,      "neighborhoods": MADRID_NEIGHBORHOODS,      "osm_name": "Madrid"},
    "barcelona":   {"name": "Barcelona",   "country": "Spain",          "bbox": BARCELONA_BBOX,   "center": BARCELONA_CENTER,   "radius_m": BARCELONA_SEARCH_RADIUS_M,   "districts": BARCELONA_DISTRICTS,   "neighborhoods": BARCELONA_NEIGHBORHOODS,   "osm_name": "Barcelona"},
    "seville":     {"name": "Seville",     "country": "Spain",          "bbox": SEVILLE_BBOX,     "center": SEVILLE_CENTER,     "radius_m": SEVILLE_SEARCH_RADIUS_M,     "districts": SEVILLE_DISTRICTS,     "neighborhoods": SEVILLE_NEIGHBORHOODS,     "osm_name": "Sevilla"},
    "valencia":    {"name": "Valencia",    "country": "Spain",          "bbox": VALENCIA_BBOX,    "center": VALENCIA_CENTER,    "radius_m": VALENCIA_SEARCH_RADIUS_M,    "districts": VALENCIA_DISTRICTS,    "neighborhoods": VALENCIA_NEIGHBORHOODS,    "osm_name": "València"},
    "bilbao":      {"name": "Bilbao",      "country": "Spain",          "bbox": BILBAO_BBOX,      "center": BILBAO_CENTER,      "radius_m": BILBAO_SEARCH_RADIUS_M,      "districts": BILBAO_DISTRICTS,      "neighborhoods": BILBAO_NEIGHBORHOODS,      "osm_name": "Bilbao"},
    "malaga":      {"name": "Málaga",      "country": "Spain",          "bbox": MALAGA_BBOX,      "center": MALAGA_CENTER,      "radius_m": MALAGA_SEARCH_RADIUS_M,      "districts": MALAGA_DISTRICTS,      "neighborhoods": MALAGA_NEIGHBORHOODS,      "osm_name": "Málaga"},
    # Portugal
    "lisbon":      {"name": "Lisbon",      "country": "Portugal",       "bbox": LISBON_BBOX,      "center": LISBON_CENTER,      "radius_m": LISBON_SEARCH_RADIUS_M,      "districts": LISBON_DISTRICTS,      "neighborhoods": LISBON_NEIGHBORHOODS,      "osm_name": "Lisboa"},
    "porto":       {"name": "Porto",       "country": "Portugal",       "bbox": PORTO_BBOX,       "center": PORTO_CENTER,       "radius_m": PORTO_SEARCH_RADIUS_M,       "districts": PORTO_DISTRICTS,       "neighborhoods": PORTO_NEIGHBORHOODS,       "osm_name": "Porto"},
    "faro":        {"name": "Faro",        "country": "Portugal",       "bbox": FARO_BBOX,        "center": FARO_CENTER,        "radius_m": FARO_SEARCH_RADIUS_M,        "districts": FARO_DISTRICTS,        "neighborhoods": FARO_NEIGHBORHOODS,        "osm_name": "Faro"},
    # Poland
    "warsaw":      {"name": "Warsaw",      "country": "Poland",         "bbox": WARSAW_BBOX,      "center": WARSAW_CENTER,      "radius_m": WARSAW_SEARCH_RADIUS_M,      "districts": WARSAW_DISTRICTS,      "neighborhoods": WARSAW_NEIGHBORHOODS,      "osm_name": "Warszawa"},
    "krakow":      {"name": "Kraków",      "country": "Poland",         "bbox": KRAKOW_BBOX,      "center": KRAKOW_CENTER,      "radius_m": KRAKOW_SEARCH_RADIUS_M,      "districts": KRAKOW_DISTRICTS,      "neighborhoods": KRAKOW_NEIGHBORHOODS,      "osm_name": "Kraków"},
    "wroclaw":     {"name": "Wrocław",     "country": "Poland",         "bbox": WROCLAW_BBOX,     "center": WROCLAW_CENTER,     "radius_m": WROCLAW_SEARCH_RADIUS_M,     "districts": WROCLAW_DISTRICTS,     "neighborhoods": WROCLAW_NEIGHBORHOODS,     "osm_name": "Wrocław"},
    "gdansk":      {"name": "Gdańsk",      "country": "Poland",         "bbox": GDANSK_BBOX,      "center": GDANSK_CENTER,      "radius_m": GDANSK_SEARCH_RADIUS_M,      "districts": GDANSK_DISTRICTS,      "neighborhoods": GDANSK_NEIGHBORHOODS,      "osm_name": "Gdańsk"},
    "poznan":      {"name": "Poznań",      "country": "Poland",         "bbox": POZNAN_BBOX,      "center": POZNAN_CENTER,      "radius_m": POZNAN_SEARCH_RADIUS_M,      "districts": POZNAN_DISTRICTS,      "neighborhoods": POZNAN_NEIGHBORHOODS,      "osm_name": "Poznań"},
}

# backwards compat
NEIGHBORHOODS = PRAGUE_NEIGHBORHOODS

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

