from flask import Flask, send_from_directory
import os

app = Flask(__name__)
svelte_build_dir = '../room-vis/build'


# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory(svelte_build_dir, 'index.html')


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory(svelte_build_dir, path)


if __name__ == "__main__":
    app.run(debug=True)
