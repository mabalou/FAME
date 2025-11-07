from datetime import datetime
from pathlib import Path
import csv

def registrar_visita(pagina, theme, lang):
    """Guarda una nueva visita en data/visitas.csv"""
    logs_file = Path("data/visitas.csv")
    logs_file.parent.mkdir(exist_ok=True)

    if not logs_file.exists():
        with open(logs_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["fecha","hora","pagina","tema","idioma","ciudad","region","pais","coordenadas"])

    try:
        import requests
        r = requests.get("https://ipinfo.io/json", timeout=3)
        if r.status_code == 200:
            info = r.json()
            ciudad = info.get("city", "Desconocido")
            region = info.get("region", "")
            pais = info.get("country", "")
            loc = info.get("loc", "")
        else:
            ciudad, region, pais, loc = "Desconocido", "", "", ""
    except Exception:
        ciudad, region, pais, loc = "Desconocido", "", "", ""

    now = datetime.now()
    with open(logs_file, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S"),
            pagina, theme, lang, ciudad, region, pais, loc
        ])

def total_visitas():
    """Devuelve el número total de visitas registradas"""
    try:
        logs_file = Path("data/visitas.csv")
        if not logs_file.exists():
            return 0
        with open(logs_file, "r", encoding="utf-8") as f:
            return max(0, sum(1 for _ in f) - 1)
    except Exception:
        return 0
