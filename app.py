"""
app.py
======
Punto de entrada de la aplicación. Solo contiene:
  - Configuración de Flask
  - Rutas (qué URL hace qué)
  - Gestión de sesión (guardar/leer token)

La lógica de Spotify está en spotify_api.py
Las variables de entorno están en config.py
"""

import logging
from flask import Flask, render_template, request, redirect, session, url_for, abort

import config
import spotify_api

# ── Configuración de la aplicación ───────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# ── Helpers de sesión ─────────────────────────────────────────────────────────

def get_authenticated_client():
    """
    Intenta obtener un cliente de Spotify autenticado desde la sesión.
    Si no hay token o no se puede renovar, devuelve None.

    Uso en cualquier ruta protegida:
        sp = get_authenticated_client()
        if not sp:
            return redirect(url_for("login"))
    """
    token_info = session.get("token_info")
    if not token_info:
        return None

    try:
        token_info = spotify_api.refresh_token_if_expired(token_info)
        session["token_info"] = token_info  # Guardar si se renovó
        return spotify_api.get_client(token_info)
    except Exception:
        logger.exception("Error al obtener cliente de Spotify")
        session.clear()
        return None


# ── Rutas públicas ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    featured_albums = spotify_api.get_featured_albums(limit=10)
    return render_template("index.html", featured_albums=featured_albums)


# ── Rutas de autenticación ────────────────────────────────────────────────────

@app.route("/login")
def login():
    oauth = spotify_api.create_oauth()
    auth_url = oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        logger.warning("Callback recibido sin código de autorización")
        return redirect(url_for("index"))

    oauth = spotify_api.create_oauth()
    token_info = oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# ── Rutas protegidas (requieren login) ────────────────────────────────────────

@app.route("/profile")
def profile():
    sp = get_authenticated_client()
    if not sp:
        return redirect(url_for("login"))

    try:
        user          = spotify_api.get_user_profile(sp)
        top_tracks    = spotify_api.get_top_tracks(sp, limit=10)
        top_artists   = spotify_api.get_top_artists(sp, limit=10)
        recent_tracks = spotify_api.get_recent_tracks(sp, limit=10)
        followed      = spotify_api.get_followed_artists(sp, limit=10)
    except Exception:
        logger.exception("Error al cargar el perfil")
        abort(503)

    return render_template(
        "profile.html",
        user=user,
        top_tracks=top_tracks,
        top_artists=top_artists,
        recent_tracks=recent_tracks,
        followed_artists=followed,
    )


@app.route("/stats/<time_range>")
def stats(time_range):
    if time_range not in config.VALID_TIME_RANGES:
        return redirect(url_for("profile"))

    sp = get_authenticated_client()
    if not sp:
        return redirect(url_for("login"))

    try:
        user        = spotify_api.get_user_profile(sp)
        top_tracks  = spotify_api.get_top_tracks(sp, time_range=time_range, limit=20)
        top_artists = spotify_api.get_top_artists(sp, time_range=time_range, limit=20)
        top_genres  = spotify_api.get_genre_breakdown(top_artists, top_n=10)
    except Exception:
        logger.exception("Error al cargar estadísticas para %s", time_range)
        abort(503)

    return render_template(
        "detailed_stats.html",
        user=user,
        top_tracks=top_tracks,
        top_artists=top_artists,
        top_genres=top_genres,
        time_range=time_range,
        time_range_name=config.VALID_TIME_RANGES[time_range],
    )


# ── Páginas de error ──────────────────────────────────────────────────────────

@app.errorhandler(503)
def service_unavailable(e):
    return render_template("error.html", message="No se pudo conectar con Spotify. Intenta de nuevo en unos segundos."), 503

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Esta página no existe."), 404


# ── Arranque ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=config.FLASK_DEBUG, host="127.0.0.1", port=5000)