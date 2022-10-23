from os import abort
import random
import asyncio
import sqlite3
import textwrap
from unittest import result
import databases
import dataclasses
from paramiko import PasswordRequiredException
from sqlalchemy import all_, values
import toml
from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

app.config.from_file(f"./etc/{__name__}.toml", toml.load)

@dataclasses.dataclass
class User:
    username: str
    password: str

@dataclasses.dataclass
class Id:
    user_id: str
    game_id: int
    secret_word_id: int

@dataclasses.dataclass
class Play:
    play_id: int
    game_id: int
    guessed_word: str
    cr_lt_cr_pl: str
    cr_lt_wr_pl: str

#    def __init__(self):
#        self.user_id = 'None'
#        self.user_pass = 'None'
#        self.play_id = 0
#        self.word_id = 0
#        self.game_id = 0

# connect to the DB
async def _connect_db():
    database = databases.Database(app.config["DATABASES"]["URL"])
    await database.connect()
    return database

#Get DB
def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db

@app.errorhandler(401)
def invalid_user():
    return {"error": "The Username or password is invalid,Try again!!"}, 401

@app.route('/', methods=["GET"])
async def intro():
    prompt = 'Welcome to our version of wordle'
    return prompt


@app.route('/signup', methods=["GET", "POST"])
@validate_request(User)
async def signUp(data):
    # _get_db() to fetch the db connection
    db = await _get_db()
    user = dataclasses.asdict(data)

    try:
        newU = await db.execute(
            """INSERT INTO user(user_id, user_pass) VALUES (:username, :password)
            """,
            user,
        )

    except sqlite3.IntegrityError as e:
        abort(401,e)

    return user, {"Message": "User has been created succesfully"}, 201

async def verify_user(db, authorization):
    if authorization is not None:
    #    print(authorization.type + "Name: "+authorization.username+"Password: "+authorization.password)

        if authorization is not None and authorization.type == 'basic':
            responseFromDB = await db.fetch_one("SELECT user_id FROM users where usr_id :username user_pass=:password",
                                                values={"username": authorization.username, "password": authorization.password})
            app.logger.debug(type(responseFromDB))
            if responseFromDB:
                return responseFromDB.user_id
            else:
                #print("Error with the username or password")
                abort(401)
        else:
            abort(401)

@app.route("/signin", methods=["GET"])
async def signIn():
    db = await _get_db()
    await verify_user(db, request.authorization)

    response = {"authenticated": True}
    return response, 200
    # db = await _get_db()
    # user = dataclasses.asdict(pl)
    # suBool = True
    # while suBool:
    #     pl.user_id = input('Please enter a username: ')
    #     pl.user_pass = input('Please enter a password: ')
    #     con = await _get_db()
    #     db = con.cursor()
    #     holder = db.execute("SELECT user_id FROM user WHERE user_id=:user",{'user': pl.user_id})
    #     name = holder.fetchone()
    #     holder = db.execute("SELECT user_pass FROM user WHERE user_id=:user",{'user': pl.user_id})
    #     Password = holder.fetchone()
    #     if name == None:
    #         print('Welcome new user!')
    #         db.execute("INSERT INTO user (user_id, user_pass) VALUES(?, ?)",(pl.user_id, pl.user_pass))
    #         con.commit()
    #         suBool = False
    #     elif pl.user_pass == Password[0]:
    #         print('Welcome back')
    #         suBool = False
    #     else:
    #         print('This password does not match this username...')


@app.route('/DisplayGames/<string:user>', methods=["GET"])
async def displaygames(user):
    db = await _get_db()

    tempUser = await db.fetch_one("SELECT user_id FROM user WHERE user_id=:user", values={"user":user})
    if tempUser: # Exists
        gameList = await db.fetch_all("SELECT * FROM id WHERE user_id=:user", values={"user":user})
        if len(gameList) == 0:
            return {"Message": "No games found under this username..."}, 406

        return list(map(dict,gameList)), {"Message": "Games were found under this username" }, 201
    else:
        abort(404)


@app.route('/LoadGame/<string:user>/<int:gID>', methods=["GET"])
async def loadgame(user, gID):
    db = await _get_db()

    tempUser = await db.fetch_one("SELECT user_id FROM user WHERE user_id=:user", values={"user":user})
    if tempUser: # Exists
        play = await db.fetch_all("SELECT * FROM play WHERE game_id=:gID", values={"gID":gID})
        if len(play) == 0:
            return {"Message": "No plays active for the game id..."}, 406

        return list(map(dict,play)), {"Message": "Displaying current plays under this game id" }, 201
    else:
        abort(404)

@app.route('/CreateGame', methods=["POST"])
@validate_request(Id)
async def creategame(data):
    db = await _get_db()
    tempUser = dataclasses.asdict(data)
    tempUser2 = await db.fetch_one("SELECT user_id FROM user WHERE user_id=:user", values={"user":tempUser})

    if tempUser2: # Exists
        randy = random.randint(0, 2309)
        newWord = await db.fetch_one("SELECT secret_word FROM secret WHERE secret_word_id=:randInt", values={"randInt":randy})

        newGame = await db.execute("INSERT INTO id(game_id, user_id, secret_word_id) VALUES (:gID, :uID, :swID)", (None, tempUser2, randy))
        tempgID = await db.fetch_one("SELECT game_id FROM id WHERE guessed_word=:newWord", values={"newWord":newWord})
        newPlay = await db.execute("INSERT INTO play(play_id, game_id, guessed_word, cr_lt_cr_pl, cr_lt_wr_pl) VALUES (:pID, :gID, :gW, :cr, :wr)", (0, tempgID, '-----', '-----', '-'))
        return {"Message": "Created new game and play"}, 201
    else:
        abort(404)
#     cgBool = True
#     while cgBool:
#         con = await _get_db()
#         db = con.cursor()
#         holder = db.execute("SELECT game_id FROM id WHERE user_id=:user",{'user': pl.user_id})
#         ans = holder.fetchall()
#         print("Please input the number of the game you would like to play or type '0' for new game: ")
#         arr = []
#         for i in ans:
#             arr.append(i[0])
#         print(arr)
#         value = input("Select your game: ")
#         valInt = int(value)
#         con.commit()
#
#         # needs to be in while
#         if valInt == 0:
#             print("Creating new game")
#             pl.word_id = random.randint(0, 2309)
#             con = await _get_db()
#             db = con.cursor()
#             db.execute("INSERT INTO id (game_id, user_id, secret_word_id) VALUES(?, ?, ?)", (None, pl.user_id, pl.word_id))
#             holder = db.execute("SELECT game_id FROM id WHERE secret_word_id=:word",{'word': pl.word_id})
#             newWord = holder.fetchone()
#             pl.game_id = newWord[0]
#             con.commit()
#             con = await _get_db()
#             db = con.cursor()
#             db.execute("INSERT INTO play (play_id, game_id, guessed_word, cr_lt_cr_pl, cr_lt_wr_pl) VALUES(?, ?, ?, ?, ?)", (0, pl.game_id, '-----', '-----', None))
#             con.commit()
#             cgBool = False
#         elif valInt not in arr:
#             print("Invalid input")
#         else:
#             print("Loading Game")
#             pl.game_id = valInt
#             secWord = db.execute("SELECT secret_word_id FROM id WHERE game_id=:game", {'game': pl.game_id})
#             secWord2 = secWord.fetchone()
#             pl.word_id = secWord2[0]
#             cgBool = False
#
#
# @app.route('/play')
# # needs a for loop for multiple guesses
# async def play(pl):
#     con = await _get_db()
#     db = con.cursor()
#     playBool = True
#     while playBool:
#         # gets the entire row
#         holder = db.execute("SELECT * FROM play WHERE game_id=:gamenum", {'gamenum': pl.game_id})
#         gameStates = holder.fetchall()
#         print(gameStates)
#         # gets the secret word
#         cr_word = db.execute("SELECT secret_word FROM secret WHERE secret_word_id=:word", {'word' : pl.word_id})
#         cr_word2 = cr_word.fetchone()
#         cr_word3 = str(cr_word2)
#         print(cr_word3)
#         # user input
#         guess = input("Try and guess the word: ")
#
#         # check if word is real
#         ch = db.execute("SELECT correct_word FROM correct WHERE correct_word=:word", {'word': guess})
#         check = ch.fetchone()
#         print(check)
#
#         if cr_word3 == guess:
#             print('Correct!!!')
#         #    db.execute("DELETE FROM play WHERE play_id=:id", {'id': pl.play_id})
#         #    db.execute("DELETE FROM id WHERE game_id=:id", {'id': pl.play_id})
#             con.commit()
#             break
#         elif check == None:
#             print("Invalid input. Must be a real word")
#         else:
#             for i in cr_word:
#                 #check each letter for each word
#                 pass


#def main():
#    player = User()
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(asyncio.gather(
#        intro(),
#
#        signup(player),
#        choosegame(player),
#        play(player)
#    ))

#main()
app.run()
