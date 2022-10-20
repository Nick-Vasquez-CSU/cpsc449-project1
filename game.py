# from requests import put
import dataclasses

from quart import Quart, request, jsonify, abort, g
from sqlalchemy.testing.pickleable import User

import Login
app = Quart(__name__)

#to POST Login signup
@app.route("/signup", methods=["POST"])
@Login.validate_request(User)
async def signUp(data):
    # _get_db() to fetch the db connection
    db = await Login._get_db()
    user = dataclasses.asdict(data)

    try:
        await db.execute(
            """INSERT INTO users(user_id, user_pass) values (:username, :password)
            """,
            user
        )

    except sqlite3.IntegrityError as e:
        Login.abort(409,e)

    return {"Message": "User has been created succesfully"}, 201

#to GET Login signin
@app.route("/signin", methods=["GET"])
async def signIn():
    db = await Login._get_db()
    await Login.verify_user(db, request.authorization)

    response = {"authenticated": True}
    return response, 200
#to GET creation of new word

#to GET list of games

#to POST the game details

#to DELETE the game data

import sqlite3


bool_ = False

conn = sqlite3.connect('API_DATA.db')

dB = conn.cursor()
holder = dB.execute('SELECT cor_word FROM TEST2')
ans = str(holder.fetchone())
answer = ans[2:8]
print(answer)

def check_word(input):
    if input == answer: return True




while bool_ != True:

    # initial prompt for game
    game_id = dB.execute('SELECT game_id FROM TEST2')
    print('Game ID', game_id)

    trys_left = dB.execute('SELECT trys_left FROM TEST2')
    print('Trys left', trys_left.fetchone())

    cor_pos = dB.execute('SELECT cor_pos FROM TEST2')
    print('Correct Position', cor_pos.fetchone())

    cor_let = dB.execute('SELECT cor_let FROM TEST2')
    print('Correct letters', cor_let.fetchone())


    x = 'Try and guess the word: '
    y = input(x)

    if y == 'EXIT':
        break

    bool_ = check_word(y)
