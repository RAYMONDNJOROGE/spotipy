from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

app = Flask(__name__)

# Use environment variables, fallback to hardcoded values for testing
client_id = os.getenv("SPOTIPY_CLIENT_ID", "36f9c27a476441b998215a3e7d320dc7")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET", "3c64f512eaae4daa9fffafac8ec3f871")

# Authenticate with Spotify API
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

@app.route("/", methods=["GET", "POST"])
def index():
    track = None
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            result = sp.search(q=query, type="track", limit=1)
            items = result.get("tracks", {}).get("items", [])
            if items:
                track = items[0]
    return render_template("index.html", track=track)

if __name__ == "__main__":
    app.run(debug=True)