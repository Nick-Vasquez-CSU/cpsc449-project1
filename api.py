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

class User:
    def __init__(self):
        self.user_id = 'None'
        self.user_pass = 'None'
        self.play_id = 0
        self.word_id = 0
        self.game_id = 0

# connect to the DB
async def _get_db():
    conn = sqlite3.connect('var/wordle.db')
    return conn

@app.route('/')
async def intro():
    prompt = 'Welcome to our version of wordle'
    print(prompt)


@app.route('/signup')
async def signup(pl):
    suBool = True
    while suBool:
        pl.user_id = input('Please enter a username: ')
        pl.user_pass = input('Please enter a password: ')
        con = await _get_db()
        db = con.cursor()
        holder = db.execute("SELECT user_id FROM user WHERE user_id=:user",{'user': pl.user_id})
        name = holder.fetchone()
        holder = db.execute("SELECT user_pass FROM user WHERE user_id=:user",{'user': pl.user_id})
        Password = holder.fetchone()
        if name == None:
            print('Welcome new user!')
            db.execute("INSERT INTO user (user_id, user_pass) VALUES(?, ?)",(pl.user_id, pl.user_pass))
            con.commit()
            suBool = False
        elif pl.user_pass == Password[0]:
            print('Welcome back')
            suBool = False
        else:
            print('This password does not match this username...')


@app.route('/ChooseGame')
async def choosegame(pl):
    cgBool = True
    while cgBool:
        con = await _get_db()
        db = con.cursor()
        holder = db.execute("SELECT game_id FROM id WHERE user_id=:user",{'user': pl.user_id})
        ans = holder.fetchall()
        print("Please input the number of the game you would like to play or type '0' for new game: ")
        arr = []
        for i in ans:
            arr.append(i[0])
        print(arr)
        value = input("Select your game: ")
        valInt = int(value)


        # needs to be in while
        if valInt == 0:
            print("Creating new game")
            pl.word_id = random.randint(0, 2309)
            db.execute("INSERT INTO id (game_id, user_id, secret_word_id) VALUES(?, ?, ?)", (None, pl.user_id, pl.word_id))
            holder = db.execute("SELECT game_id FROM id WHERE secret_word_id=:word",{'word': pl.word_id})
            newWord = holder.fetchone()
            pl.game_id = newWord[0]
            db.execute("INSERT INTO play (play_id, game_id, guessed_word, cr_lt_cr_pl, cr_lt_wr_pl) VALUES(?, ?, ?, ?, ?)", (0, pl.game_id, '-----', '-----', None))
            con.commit()
            cgBool = False
        elif valInt not in arr:
            print("Invalid input")
        else:
            print("Loading Game")
            pl.game_id = valInt
            secWord = db.execute("SELECT secret_word_id FROM id WHERE game_id=:game", {'game': pl.game_id})
            secWord2 = secWord.fetchone()
            pl.word_id = secWord2[0]
            cgBool = False


@app.route('/play')
# needs a for loop for multiple guesses
async def play(pl):
    con = await _get_db()
    db = con.cursor()
    playBool = True
    while playBool:
        # gets the entire row
        holder = db.execute("SELECT * FROM play WHERE game_id=:gamenum", {'gamenum': pl.game_id})
        gameStates = holder.fetchall()
        print(gameStates)
        # gets the secret word
        cr_word = db.execute("SELECT secret_word FROM secret WHERE secret_word_id=:word", {'word' : pl.word_id})
        cr_word2 = cr_word.fetchone()
        cr_word3 = cr_word2[2:6]
        print(cr_word3)
        # user input
        guess = input("Try and guess the word: ")

        # check if word is real
        ch = db.execute("SELECT correct_word FROM correct WHERE correct_word=:word", {'word': guess})
        check = ch.fetchone()
        print(check)

        if cr_word3 == guess:
            print('Correct!!!')
        #    db.execute("DELETE FROM play WHERE play_id=:id", {'id': pl.play_id})
        #    db.execute("DELETE FROM id WHERE game_id=:id", {'id': pl.play_id})
            con.commit()
            break
        elif check == None:
            print("Invalid input. Must be a real word")
        else:
            for i in cr_word:
                #check each letter for each word
                pass


def main():
    player = User()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        intro(),

        signup(player),
        choosegame(player),
        play(player)
    ))

main()
