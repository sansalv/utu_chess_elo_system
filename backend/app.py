from flask import Flask
from flask import send_file
from markupsafe import escape
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route("/")
def main_page():
    return( "<h>UTU chess backend api</h> \
     <p>/api/players for players_db.json</p> \
     <p>(TODO) /api/players/<id> for data of player with unique id</p>")


@app.route("/api/players")
def sendAllPlayersData():
    return send_file('../players_database.json')

@app.route('/api/players/<id>')
def sendSinglePlayerData(id):
    # show the user profile for that user
    return f'Player with unique id {escape(id)}'

    