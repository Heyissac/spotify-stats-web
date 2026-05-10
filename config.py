import os
from dotenv import load_dotenv

load_dotenv()

# ── Aplicación ────────────────────────────────────────────────────────────────

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError(
        "Falta la variable de entorno SECRET_KEY. "
        "Añádela a tu archivo .env antes de iniciar el servidor."
    )

FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"

# ── Spotify ───────────────────────────────────────────────────────────────────

SPOTIFY_CLIENT_ID     = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI  = os.environ.get("SPOTIFY_REDIRECT_URI", "http://localhost:5000/callback")

SPOTIFY_SCOPE = (
    "user-top-read "
    "user-read-recently-played "
    "user-read-email "
    "user-follow-read"
)

# Períodos de tiempo válidos para la API de Spotify
VALID_TIME_RANGES = {
    "short_term":  "Últimas 4 semanas",
    "medium_term": "Últimos 6 meses",
    "long_term":   "Varios años",
}

# Artistas usados para poblar la sección de álbumes en el index
FEATURED_ARTISTS = [
    "Taylor Swift", "Bad Bunny", "Drake", "The Weeknd",
    "Ed Sheeran", "Ariana Grande", "Billie Eilish",
    "Post Malone", "Dua Lipa", "Harry Styles",
]