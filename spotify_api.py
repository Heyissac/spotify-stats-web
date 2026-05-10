"""
spotify_api.py
==============
Toda la comunicación con la API de Spotify vive aquí.
Este archivo no sabe nada de Flask, rutas ni templates.

Funciones públicas (las que importa app.py):
    create_oauth()              → SpotifyOAuth configurado
    get_client(token_info)      → Spotify autenticado con el token del usuario
    refresh_token_if_expired()  → Devuelve token_info actualizado si venció
    get_user_profile()          → Info básica del usuario
    get_top_tracks()            → Top canciones del usuario
    get_top_artists()           → Top artistas del usuario
    get_recent_tracks()         → Historial reciente
    get_followed_artists()      → Artistas seguidos
    get_genre_breakdown()       → Análisis de géneros a partir de artistas
    get_featured_albums()       → Álbumes para la portada (Client Credentials)
"""

import logging
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

import config

logger = logging.getLogger(__name__)


# ── Autenticación ─────────────────────────────────────────────────────────────

def create_oauth() -> SpotifyOAuth:
    """Devuelve un objeto SpotifyOAuth listo para usarse en login y callback."""
    return SpotifyOAuth(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=config.SPOTIFY_REDIRECT_URI,
        scope=config.SPOTIFY_SCOPE,
        show_dialog=True,
    )


def get_client(token_info: dict) -> spotipy.Spotify:
    """
    Recibe el token_info guardado en sesión y devuelve un cliente de Spotify
    autenticado. No renueva el token; para eso usa refresh_token_if_expired().
    """
    return spotipy.Spotify(auth=token_info["access_token"])


def refresh_token_if_expired(token_info: dict) -> dict:
    """
    Comprueba si el token venció y lo renueva si es necesario.
    Devuelve siempre un token_info válido (el mismo u uno nuevo).

    Uso típico en app.py:
        token_info = refresh_token_if_expired(session["token_info"])
        session["token_info"] = token_info
    """
    oauth = create_oauth()
    if oauth.is_token_expired(token_info):
        logger.info("Token expirado, renovando...")
        token_info = oauth.refresh_access_token(token_info["refresh_token"])
    return token_info


# ── Datos del usuario ─────────────────────────────────────────────────────────

def get_user_profile(sp: spotipy.Spotify) -> dict:
    """Perfil básico: nombre, foto, email, país."""
    return sp.current_user()


def get_top_tracks(sp: spotipy.Spotify, time_range: str = "medium_term", limit: int = 20) -> list:
    """
    Top canciones del usuario.

    Args:
        time_range: "short_term" | "medium_term" | "long_term"
        limit: entre 1 y 50
    """
    result = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return result.get("items", [])


def get_top_artists(sp: spotipy.Spotify, time_range: str = "medium_term", limit: int = 20) -> list:
    """
    Top artistas del usuario.

    Args:
        time_range: "short_term" | "medium_term" | "long_term"
        limit: entre 1 y 50
    """
    result = sp.current_user_top_artists(limit=limit, time_range=time_range)
    return result.get("items", [])


def get_recent_tracks(sp: spotipy.Spotify, limit: int = 20) -> list:
    """Historial de reproducción reciente."""
    result = sp.current_user_recently_played(limit=limit)
    return result.get("items", [])


def get_followed_artists(sp: spotipy.Spotify, limit: int = 10) -> list:
    """Artistas que el usuario sigue."""
    result = sp.current_user_followed_artists(limit=limit)
    return result.get("artists", {}).get("items", [])


def get_genre_breakdown(artists: list, top_n: int = 10) -> list[tuple[str, int]]:
    """
    Analiza los géneros de una lista de artistas y devuelve los más frecuentes.

    Args:
        artists: lista devuelta por get_top_artists()
        top_n: cuántos géneros incluir en el resultado

    Returns:
        Lista de tuplas ordenadas: [("pop", 5), ("reggaeton", 3), ...]
    """
    genres: dict[str, int] = {}
    for artist in artists:
        for genre in artist.get("genres", []):
            genres[genre] = genres.get(genre, 0) + 1
    return sorted(genres.items(), key=lambda x: x[1], reverse=True)[:top_n]


# ── Contenido público (sin autenticación del usuario) ─────────────────────────

def get_featured_albums(limit: int = 10) -> list[dict]:
    """
    Obtiene álbumes recientes de artistas populares usando Client Credentials
    (no requiere que el usuario esté logueado).

    Cada álbum del resultado tiene las claves:
        name, artist, image, url, release_date

    Si la API falla, devuelve lista vacía y registra el error.
    """
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=config.SPOTIFY_CLIENT_ID,
                client_secret=config.SPOTIFY_CLIENT_SECRET,
            )
        )
        return _fetch_albums_from_artists(sp, config.FEATURED_ARTISTS, limit)
    except Exception:
        logger.exception("Error al obtener álbumes destacados")
        return []


def _fetch_albums_from_artists(
    sp: spotipy.Spotify,
    artist_names: list[str],
    limit: int,
) -> list[dict]:
    """
    Función interna: itera artistas y recopila sus álbumes hasta alcanzar el límite.
    El guion bajo al inicio indica que solo debe usarse dentro de este archivo.
    """
    albums: list[dict] = []
    seen_ids: set[str] = set()

    for artist_name in artist_names:
        if len(albums) >= limit:
            break

        search = sp.search(q=artist_name, type="artist", limit=1)
        artists_found = search.get("artists", {}).get("items", [])
        if not artists_found:
            continue

        artist_id = artists_found[0]["id"]
        raw_albums = sp.artist_albums(artist_id, album_type="album", limit=3)

        for album in raw_albums.get("items", []):
            if len(albums) >= limit:
                break

            album_id = album.get("id")
            if not album_id or album_id in seen_ids:
                continue

            seen_ids.add(album_id)
            albums.append({
                "name":         album.get("name", "Álbum desconocido"),
                "artist":       album.get("artists", [{}])[0].get("name", "Artista desconocido"),
                "image":        album.get("images", [{}])[0].get("url") if album.get("images") else None,
                "url":          album.get("external_urls", {}).get("spotify", "#"),
                "release_date": album.get("release_date", ""),
            })

    return albums