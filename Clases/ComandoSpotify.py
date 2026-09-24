import os
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

class ComandoSpotify:

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

    SCOPE = (
        "user-read-playback-state "
        "user-modify-playback-state"
    )

    @staticmethod
    def conectar():

        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=ComandoSpotify.CLIENT_ID,
                client_secret=ComandoSpotify.CLIENT_SECRET,
                redirect_uri=ComandoSpotify.REDIRECT_URI,
                scope=ComandoSpotify.SCOPE
            )
        )

    @staticmethod
    def abrir_spotify():

        import subprocess

        subprocess.Popen(
            "spotify",
            shell=True
        )

    @staticmethod
    def reproducir_cancion_spotify(texto):

        texto = texto.lower().strip()

        if "reproducir" in texto:
            cancion = texto.split("reproducir", 1)[1].strip()

        elif "reproduce" in texto:
            cancion = texto.split("reproduce", 1)[1].strip()

        else:
            return

        if not cancion:
            return

        print(f"🎵 Buscando: {cancion}")

        spotify = ComandoSpotify.conectar()

        resultados = spotify.search(
            q=cancion,
            type="track",
            limit=1
        )

        tracks = resultados["tracks"]["items"]

        if not tracks:
            print("❌ No encontré la canción")
            return

        track = tracks[0]

        nombre = track["name"]
        artista = track["artists"][0]["name"]
        uri = track["uri"]

        print(f"🎵 Encontrado: {nombre} - {artista}")
        print(f"URI: {uri}")

        spotify.start_playback(
            uris=[uri]
        )

        print("▶️ Reproduciendo")