# server/app.py

from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()] 
    games = [] #empty array to populate games into
    for game in Game.query.all():
        game_dict = game.to_dict()
        # game_dict = { #this line of code constructs a dictionary (game_dict) where information about a game (such as title, genre, platform, and price) is stored with specific keys for easy access and organization. This dictionary is then used to represent each game in a structured format, making it convenient to work with and manipulate the data. 
        #     "title": game.title,
        #     "genre": game.genre,
        #     "platform": game.platform,
        #     "price": game.price,
        # }
        games.append(game_dict)
    response = make_response(games, 200, {"Content-Type": "application/json"})
     #in your response headers, you're telling the client that the content being sent in the response body is in JSON format. This is important for the client to know so that it can properly parse and handle the response data. When a client receives a response with this header, it knows that it's receiving JSON data and can parse it accordingly.
    return response
#The line for game in Game.query.all(): loops over all existing game data retrieved from the SQL database.
# Each game within this loop represents one instance of the Game model from the database.
# The game_dict is then constructed for each game instance, containing attributes such as title, genre, platform, and price.
# These attributes are then accessible through the keys of game_dict.
# Finally, the information from each game_dict is appended to the games list, which is later converted into a JSON response.
# Finally we convert/serializes it into JSON data and set the status as 200. 


@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    # game_dict = {
    #     "title": game.title,
    #     "genre": game.genre,
    #     "platform": game.platform,
    #     "price": game.price,
    # }

    # game_dict = game.to_dict() #.to_dict() is a common method used to convert objects into dictionaries, making them easier to work with in various contexts, such as serialization, data manipulation, and web development.
    
     # use association proxy to get users for a game
    users = [user.to_dict(rules=("-reviews",)) for user in game.users]
    response = make_response(
        users,
        200
    )
    

    # When we're using the jsonify() method, Flask serializes (converts from one format to another) the SQLAlchemy object into a JSON object by getting a list of keys and values to pass to the client. HOWEVER the .to_dict removes the need and use case of JSONIFY

    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()

    users = [review.user.to_dict(rules=('-reviews',))
             for review in game.reviews]
    response = make_response(
        users,
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

